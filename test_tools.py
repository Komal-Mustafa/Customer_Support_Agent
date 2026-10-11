from tools import get_order_status, get_order_details, process_refund, reset_password

print(get_order_status("ORD-1002"))
print(get_order_status("ord-1001"))
print(get_order_status("ORD-9999"))
print()
print(get_order_details("ORD-1006"))
print()
print(process_refund("ORD-1004", "changed my mind"))   # cancelled -> blocked
print(process_refund("ORD-1005", "damaged"))           # already refunded
print(process_refund("ORD-1002", "too late"))          # shipped -> blocked
print(process_refund("ORD-1001", "wrong size"))        # success
print(process_refund("ORD-1001", "wrong size"))        # now already refunded
print()
print(reset_password("sana@example.com"))     # locked -> unlocked
print(reset_password("bilal@example.com"))    # normal
print(reset_password("nobody@example.com"))   # not found