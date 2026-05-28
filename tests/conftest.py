"""
conftest.py — Shared fixtures and hooks for the entire test suite.

pytest-bdd resolves step definitions from any conftest.py on the path,
so common steps live here while scenario-specific ones go in their own files.
"""

import pytest
from pytest_bdd import given, when, then, parsers

from src.cart import Coupon, Product, ShoppingCart, CartError


# ════════════════════════════════════════════════════════════════════════════════
# Fixtures
# ════════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def cart() -> ShoppingCart:
    """Populated by the 'a user … has an empty shopping cart' step."""
    return None   # placeholder; replaced by the Given step below


@pytest.fixture
def product_registry() -> dict:
    """Shared dictionary that step defs write products into by name."""
    return {}


@pytest.fixture
def coupon_registry() -> dict:
    """Shared dictionary that step defs write coupons into by code."""
    return {}


@pytest.fixture
def last_error() -> dict:
    """Mutable box to capture exceptions raised inside When steps."""
    return {"error": None}


# ════════════════════════════════════════════════════════════════════════════════
# Background / shared Given steps
# ════════════════════════════════════════════════════════════════════════════════

@given(parsers.parse('a user "{user_id}" has an empty shopping cart'), target_fixture="cart")
def a_user_has_empty_cart(user_id: str) -> ShoppingCart:
    return ShoppingCart(user_id=user_id)


@given(parsers.parse('a product "{name}" priced at {price:f} with {stock:d} in stock'))
def a_product_exists(name: str, price: float, stock: int, product_registry: dict) -> None:
    product_id = name.lower().replace(" ", "_")
    product_registry[name] = Product(
        id=product_id, name=name, price=price, stock=stock
    )


@given(parsers.re(r'a coupon "(?P<code>[^"]+)" offering (?P<discount>[\d.]+)% off with minimum order (?P<minimum>[\d.]+)'))
def a_coupon_exists(code: str, discount: str, minimum: str, coupon_registry: dict) -> None:
    coupon_registry[code] = Coupon(
        code=code, discount_pct=float(discount), min_order_value=float(minimum), active=True
    )


@given(parsers.parse('an inactive coupon "{code}"'))
def an_inactive_coupon(code: str, coupon_registry: dict) -> None:
    coupon_registry[code] = Coupon(
        code=code, discount_pct=20.0, min_order_value=0.0, active=False
    )


# ════════════════════════════════════════════════════════════════════════════════
# Shared When steps
# ════════════════════════════════════════════════════════════════════════════════

@given(parsers.parse('the user adds {qty:d} "{name}" to the cart'))
@when(parsers.parse('the user adds {qty:d} "{name}" to the cart'))
def user_adds_item(qty: int, name: str, cart: ShoppingCart, product_registry: dict) -> None:
    cart.add_item(product_registry[name], quantity=qty)


@when(parsers.parse('the user tries to add {qty:d} "{name}" to the cart'))
def user_tries_to_add_item(
    qty: int, name: str, cart: ShoppingCart, product_registry: dict, last_error: dict
) -> None:
    try:
        cart.add_item(product_registry[name], quantity=qty)
    except CartError as exc:
        last_error["error"] = exc


@given(parsers.parse('the user applies coupon "{code}"'))
@when(parsers.parse('the user applies coupon "{code}"'))
def user_applies_coupon(code: str, cart: ShoppingCart, coupon_registry: dict) -> None:
    cart.apply_coupon(coupon_registry[code])


@when(parsers.parse('the user tries to apply coupon "{code}"'))
def user_tries_to_apply_coupon(
    code: str, cart: ShoppingCart, coupon_registry: dict, last_error: dict
) -> None:
    try:
        cart.apply_coupon(coupon_registry[code])
    except CartError as exc:
        last_error["error"] = exc


@when(parsers.parse('the user removes "{name}" from the cart'))
def user_removes_item(name: str, cart: ShoppingCart, product_registry: dict) -> None:
    product_id = product_registry[name].id
    cart.remove_item(product_id)


@when(parsers.parse('the user updates "{name}" quantity to {qty:d}'))
def user_updates_quantity(name: str, qty: int, cart: ShoppingCart, product_registry: dict) -> None:
    product_id = product_registry[name].id
    cart.update_quantity(product_id, qty)


@when("the user clears the cart")
def user_clears_cart(cart: ShoppingCart) -> None:
    cart.clear()


# ════════════════════════════════════════════════════════════════════════════════
# Shared Then steps
# ════════════════════════════════════════════════════════════════════════════════

@then(parsers.parse("the cart should contain {count:d} item"))
@then(parsers.parse("the cart should contain {count:d} items"))
def cart_item_count(count: int, cart: ShoppingCart) -> None:
    assert cart.item_count == count, f"Expected {count} items, got {cart.item_count}"


@then(parsers.parse("the cart subtotal should be {expected:f}"))
def cart_subtotal(expected: float, cart: ShoppingCart) -> None:
    assert cart.subtotal == pytest.approx(expected, abs=0.01), (
        f"Expected subtotal {expected}, got {cart.subtotal}"
    )


@then(parsers.parse("the cart total should be {expected:f}"))
def cart_total(expected: float, cart: ShoppingCart) -> None:
    assert cart.total == pytest.approx(expected, abs=0.01), (
        f"Expected total {expected}, got {cart.total}"
    )


@then(parsers.parse("the discount amount should be {expected:f}"))
def discount_amount(expected: float, cart: ShoppingCart) -> None:
    assert cart.discount_amount == pytest.approx(expected, abs=0.01), (
        f"Expected discount {expected}, got {cart.discount_amount}"
    )


@then("the cart should be empty")
def cart_is_empty(cart: ShoppingCart) -> None:
    assert cart.is_empty, "Cart should be empty but it still has items."


@then(parsers.parse('the cart does not contain "{name}"'))
def cart_does_not_contain(name: str, cart: ShoppingCart, product_registry: dict) -> None:
    product_id = product_registry[name].id
    assert not cart.contains(product_id), f"Cart should NOT contain '{name}'."


@then(parsers.parse('a cart error should be raised with message "{fragment}"'))
def cart_error_raised(fragment: str, last_error: dict) -> None:
    assert last_error["error"] is not None, "Expected a CartError, but none was raised."
    assert fragment in str(last_error["error"]), (
        f"Expected error containing '{fragment}', got: '{last_error['error']}'"
    )
