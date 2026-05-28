"""
E-Commerce Shopping Cart — Domain Model
"""
from dataclasses import dataclass, field
from typing import Optional


# ── Product ────────────────────────────────────────────────────────────────────

@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int
    category: str = "general"

    def is_in_stock(self) -> bool:
        return self.stock > 0


# ── Cart Item ──────────────────────────────────────────────────────────────────

@dataclass
class CartItem:
    product: Product
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        return round(self.product.price * self.quantity, 2)


# ── Coupon ─────────────────────────────────────────────────────────────────────

@dataclass
class Coupon:
    code: str
    discount_pct: float          # e.g. 10.0 = 10 %
    min_order_value: float = 0.0
    active: bool = True

    def is_applicable(self, order_total: float) -> bool:
        return self.active and order_total >= self.min_order_value


# ── Shopping Cart ──────────────────────────────────────────────────────────────

class CartError(Exception):
    pass


class ShoppingCart:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self._items: dict[str, CartItem] = {}
        self._coupon: Optional[Coupon] = None

    # ── Mutations ──────────────────────────────────────────────────────────────

    def add_item(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise CartError("Quantity must be positive.")
        if not product.is_in_stock():
            raise CartError(f"'{product.name}' is out of stock.")
        if quantity > product.stock:
            raise CartError(
                f"Only {product.stock} unit(s) of '{product.name}' available."
            )

        if product.id in self._items:
            existing = self._items[product.id]
            new_qty = existing.quantity + quantity
            if new_qty > product.stock:
                raise CartError(
                    f"Cannot add {quantity} more — only {product.stock} in stock."
                )
            existing.quantity = new_qty
        else:
            self._items[product.id] = CartItem(product=product, quantity=quantity)

    def remove_item(self, product_id: str) -> None:
        if product_id not in self._items:
            raise CartError("Item not found in cart.")
        del self._items[product_id]

    def update_quantity(self, product_id: str, quantity: int) -> None:
        if product_id not in self._items:
            raise CartError("Item not found in cart.")
        if quantity <= 0:
            self.remove_item(product_id)
            return
        item = self._items[product_id]
        if quantity > item.product.stock:
            raise CartError(
                f"Only {item.product.stock} unit(s) available."
            )
        item.quantity = quantity

    def apply_coupon(self, coupon: Coupon) -> None:
        if not coupon.active:
            raise CartError("Coupon is inactive.")
        if self.subtotal < coupon.min_order_value:
            raise CartError(
                f"Minimum order of ₹{coupon.min_order_value:.2f} required for this coupon."
            )
        self._coupon = coupon

    def clear(self) -> None:
        self._items.clear()
        self._coupon = None

    # ── Queries ────────────────────────────────────────────────────────────────

    @property
    def items(self) -> list[CartItem]:
        return list(self._items.values())

    @property
    def item_count(self) -> int:
        return sum(i.quantity for i in self._items.values())

    @property
    def subtotal(self) -> float:
        return round(sum(i.subtotal for i in self._items.values()), 2)

    @property
    def discount_amount(self) -> float:
        if self._coupon is None:
            return 0.0
        return round(self.subtotal * self._coupon.discount_pct / 100, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal - self.discount_amount, 2)

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    def contains(self, product_id: str) -> bool:
        return product_id in self._items
