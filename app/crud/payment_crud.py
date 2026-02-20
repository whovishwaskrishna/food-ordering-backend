from sqlalchemy.orm import Session
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.models.order import Order

def process_payment(db: Session, user_id:int, order_id: int):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise Exception("Order not found")
    
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()

    wallet_balance = wallet.balance if wallet else 0

    wallet_used = min(wallet_balance, order.total_amount)
    online_needed = order.total_amount - wallet_used

    # deduct wallet
    if wallet_used > 0:
        wallet.balance -= wallet_used

        tx = Transaction(
            user_id=user_id,
            order_id=order.id,
            amount=online_needed,
            type="WALLET"
        )
        db.add(tx)

    # simulate online payment
    if online_needed > 0:
        tx = Transaction(
            user_id=user_id,
            order_id=order.id,
            amount=online_needed,
            type="ONLINE"
        )
        db.add(tx)

    order.payment_status = "PAID"
    order.paid_amount = order.total_amount

    db.commit()
    return order

