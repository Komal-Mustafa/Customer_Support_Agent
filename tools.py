"""
tools.py
Function tools for the Customer Support Agent.

Plain functions (top)  -> easy to test directly
Tool versions (bottom) -> given to the agents
"""

from agents import function_tool
from data import ORDERS, USERS


# ------------------------------------------------------------
# 1. Order status
# ------------------------------------------------------------
def get_order_status(order_id: str) -> str:
    """Get the current status of a customer's order.
    Use this when the customer asks where their order is or what its status is.

    Args:
        order_id: The order ID, for example ORD-1001.
    """
    clean_id = order_id.strip().upper()
    order = ORDERS.get(clean_id)

    if order is None:
        return f"Sorry, I couldn't find order {clean_id}. Please check the ID."

    return f"Order {clean_id} is {order['status']}."


# ------------------------------------------------------------
# 2. Order details
# ------------------------------------------------------------
def get_order_details(order_id: str) -> str:
    """Get full details of an order: customer name, item, price, date and status.
    Use this when the customer asks what they ordered or how much it cost.

    Args:
        order_id: The order ID, for example ORD-1001.
    """
    clean_id = order_id.strip().upper()
    order = ORDERS.get(clean_id)

    if order is None:
        return f"Sorry, I couldn't find order {clean_id}. Please check the ID."

    return (
        f"Order {clean_id}: {order['item']} for {order['customer_name']}, "
        f"price Rs {order['price']}, ordered on {order['order_date']}, "
        f"status: {order['status']}."
    )


# ------------------------------------------------------------
# 3. Refund (business rules live here, not in the AI)
# ------------------------------------------------------------
def process_refund(order_id: str, reason: str) -> str:
    """Process a refund for a delivered order.
    Use this only when the customer clearly asks for a refund.

    Args:
        order_id: The order ID to refund.
        reason: Why the customer wants a refund.
    """
    clean_id = order_id.strip().upper()
    order = ORDERS.get(clean_id)

    # Rule 1: order must exist
    if order is None:
        return f"Sorry, I couldn't find order {clean_id}. Please check the ID."

    status = order["status"]

    # Rule 2: cancelled orders can't be refunded
    if status == "cancelled":
        return f"Order {clean_id} was cancelled, so it can't be refunded."

    # Rule 3: no double refunds
    if status == "refunded":
        return f"Order {clean_id} has already been refunded."

    # Rule 4: only delivered orders
    if status != "delivered":
        return (
            f"Order {clean_id} is still {status}. "
            "Refunds are only possible after delivery."
        )

    # Rule 5: delivered -> refund it
    order["status"] = "refunded"
    return (
        f"Refund approved for order {clean_id}. "
        f"Rs {order['price']} will be returned in 5-7 working days. "
        f"Reason noted: {reason}."
    )


# ------------------------------------------------------------
# 4. Password reset (for tech support)
# ------------------------------------------------------------
def reset_password(email: str) -> str:
    """Send a password reset link to the customer's email.
    Use this when the customer can't log in or forgot their password.

    Args:
        email: The customer's account email address.
    """
    clean_email = email.strip().lower()
    user = USERS.get(clean_email)

    if user is None:
        return f"No account found for {clean_email}. Please check the email address."

    if user["account_status"] == "locked":
        user["account_status"] = "active"
        return (
            f"The account for {clean_email} was locked. "
            "It is now unlocked, and a password reset link has been sent."
        )

    return f"A password reset link has been sent to {clean_email}."


# ------------------------------------------------------------
# 5. Approval rule: refunds of Rs 5,000 or more need a manager
# ------------------------------------------------------------
APPROVAL_LIMIT = 5000


async def refund_needs_approval(ctx, params, call_id) -> bool:
    """Return True if this refund must be approved by a human manager."""
    clean_id = str(params.get("order_id", "")).strip().upper()
    order = ORDERS.get(clean_id)
    if order is None:
        return False  # the tool itself will say "not found"
    return order["price"] >= APPROVAL_LIMIT


# ------------------------------------------------------------
# Tool versions for the agents
# (function_tool reads the name, type hints and docstring above)
# ------------------------------------------------------------
get_order_status_tool = function_tool(get_order_status)
get_order_details_tool = function_tool(get_order_details)
process_refund_tool = function_tool(process_refund, needs_approval=refund_needs_approval)
reset_password_tool = function_tool(reset_password)