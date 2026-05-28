"""
src/checkout.py — Order placement domain model
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from src.cart import ShoppingCart, CartError


class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    UPI = "upi"
    COD = "cod"              # Cash on Delivery
    WALLET = "wallet"


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"


@dataclass
class Address:
    name: str
    line1: str
    city: str
    pincode: str
    state: str


@dataclass
class Order:
    order_id: str
    user_id: str
    items: list
    subtotal: float
    discount: float
    total: float
    payment_method: PaymentMethod
    shipping_address: Address
    status: OrderStatus = OrderStatus.PENDING


class CheckoutError(Exception):
    pass


class CheckoutService:
    """Orchestrates the checkout flow."""

    def __init__(self):
        self._orders: dict[str, Order] = {}
        self._order_counter = 1000

    def place_order(
        self,
        cart: ShoppingCart,
        address: Address,
        payment_method: PaymentMethod,
    ) -> Order:
        if cart.is_empty:
            raise CheckoutError("Cannot place an order with an empty cart.")

        if not address.pincode.isdigit() or len(address.pincode) != 6:
            raise CheckoutError("Invalid pincode — must be 6 digits.")

        # Simulate payment failure for COD orders above ₹50,000
        if payment_method == PaymentMethod.COD and cart.total > 50_000:
            raise CheckoutError("COD not available for orders above ₹50,000.")

        order_id = f"ORD-{self._order_counter}"
        self._order_counter += 1

        order = Order(
            order_id=order_id,
            user_id=cart.user_id,
            items=list(cart.items),
            subtotal=cart.subtotal,
            discount=cart.discount_amount,
            total=cart.total,
            payment_method=payment_method,
            shipping_address=address,
            status=OrderStatus.CONFIRMED,
        )
        self._orders[order_id] = order
        cart.clear()          # empty the cart after successful order
        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)
