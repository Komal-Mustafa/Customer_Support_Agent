from data import ORDERS, USERS

# 1. Full details of one order
print(ORDERS["ORD-1002"])

# 2. Only the status of one order
print(ORDERS["ORD-1004"]["status"])

# 3. An order that doesn't exist (safe way)
print(ORDERS.get("ORD-9999"))

# 4. How many orders we have
print("Total orders:", len(ORDERS))