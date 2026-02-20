import time

def send_order_notification(order_id:int, user_email:str):
    time.sleep(3)

    print(f"Notification sent for order {order_id} to {user_email}")