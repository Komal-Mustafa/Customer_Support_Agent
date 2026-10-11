"""
api.py
Web API for the Customer Support agent.

POST /chat     -> send a customer message, get the agent's reply
POST /approve  -> manager approves or rejects a waiting refund
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import Runner, SQLiteSession, InputGuardrailTripwireTriggered
from triage_agent import triage_agent

app = FastAPI(title="Customer Support Agent API")

MAX_TURNS = 8

# Paused runs waiting for a manager, saved by session id
PENDING_APPROVALS = {}


# ---------- Request and response shapes (Pydantic) ----------
class ChatRequest(BaseModel):
    session_id: str
    message: str


class ApprovalRequest(BaseModel):
    session_id: str
    approve: bool


class ChatResponse(BaseModel):
    reply: str | None = None
    agent: str | None = None
    needs_approval: bool = False
    approval_details: str | None = None


# ---------- Helpers ----------
def get_session(session_id: str) -> SQLiteSession:
    """Each customer gets their own memory."""
    return SQLiteSession(session_id, "support.db")


def build_response(result, session_id: str) -> ChatResponse:
    """Turn an agent result into a clean JSON response."""
    if result.interruptions:
        # Save the paused run so /approve can continue it later
        PENDING_APPROVALS[session_id] = result.to_state()
        item = result.interruptions[0]
        return ChatResponse(
            agent=result.last_agent.name,
            needs_approval=True,
            approval_details=f"{item.name}: {item.arguments}",
        )

    return ChatResponse(
        reply=str(result.final_output),
        agent=result.last_agent.name,
    )


def handle_error(error: Exception):
    if "429" in str(error):
        raise HTTPException(status_code=429, detail="Daily AI limit reached. Please try again later.")
    raise HTTPException(status_code=500, detail="Something went wrong. Please try again.")


# ---------- Endpoints ----------
@app.get("/")
def home():
    return {"status": "ok", "message": "Customer Support Agent API is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await Runner.run(
            triage_agent,
            request.message,
            session=get_session(request.session_id),
            max_turns=MAX_TURNS,
        )
    except InputGuardrailTripwireTriggered:
        return ChatResponse(
            reply="Sorry, I can only help with orders, refunds, login and shop questions."
        )
    except Exception as error:
        handle_error(error)

    return build_response(result, request.session_id)


@app.post("/approve", response_model=ChatResponse)
async def approve(request: ApprovalRequest):
    state = PENDING_APPROVALS.pop(request.session_id, None)
    if state is None:
        raise HTTPException(status_code=404, detail="No refund is waiting for approval in this session.")

    for item in state.get_interruptions():
        if request.approve:
            state.approve(item)
        else:
            state.reject(
                item,
                rejection_message=(
                    "A manager did not approve this refund. "
                    "Politely tell the customer their refund needs further review."
                ),
            )

    try:
        result = await Runner.run(
            triage_agent,
            state,
            session=get_session(request.session_id),
            max_turns=MAX_TURNS,
        )
    except Exception as error:
        handle_error(error)

    return build_response(result, request.session_id)