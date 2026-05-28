"""
tests/step_defs/test_checkout.py

Checkout-specific step definitions and scenario bindings.
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from src.cart import ShoppingCart
from src.checkout import Address, CheckoutService, PaymentMethod, CheckoutError

scenarios("checkout.feature")


# ════════════════════════════════════════════════════════════════════════════════
# Fixtures
# ════════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def checkout_service() -> CheckoutService:
    return None   # placeholder — replaced by the Given step below


@pytest.fixture
def last_order() -> dict:
    return {"order": None}


@pytest.fixture
def checkout_error() -> dict:
    return {"error": None}


@pytest.fixture
def delivery_address() -> dict:
    return {"address": None}


# ════════════════════════════════════════════════════════════════════════════════
# Given
# ════════════════════════════════════════════════════════════════════════════════

@given("a checkout service is ready", target_fixture="checkout_service")
def a_checkout_service() -> CheckoutService:
    return CheckoutService()


@given(
    parsers.parse('a valid delivery address for "{name}" in "{city}" with pincode "{pincode}"'),
    target_fixture="delivery_address",
)
def a_valid_address(name: str, city: str, pincode: str) -> Address:
    return Address(
        name=name,
        line1="123 Main Street",
        city=city,
        pincode=pincode,
        state="India",
    )


@given(
    parsers.parse('a delivery address with invalid pincode "{pincode}"'),
    target_fixture="delivery_address",
)
def an_invalid_address(pincode: str) -> Address:
    return Address(
        name="Test User",
        line1="1 Bad Street",
        city="Nowhere",
        pincode=pincode,
        state="India",
    )


# ════════════════════════════════════════════════════════════════════════════════
# When
# ════════════════════════════════════════════════════════════════════════════════

@when(
    parsers.parse('the user checks out using "{method}"'),
)
def user_checks_out(
    method: str,
    cart: ShoppingCart,
    checkout_service: CheckoutService,
    delivery_address: Address,
    last_order: dict,
) -> None:
    order = checkout_service.place_order(
        cart,
        address=delivery_address,
        payment_method=PaymentMethod(method),
    )
    last_order["order"] = order


@when(
    parsers.parse('the user tries to check out using "{method}"'),
)
def user_tries_to_check_out(
    method: str,
    cart: ShoppingCart,
    checkout_service: CheckoutService,
    delivery_address: Address,
    checkout_error: dict,
) -> None:
    try:
        checkout_service.place_order(
            cart,
            address=delivery_address,
            payment_method=PaymentMethod(method),
        )
    except CheckoutError as exc:
        checkout_error["error"] = exc


# ════════════════════════════════════════════════════════════════════════════════
# Then
# ════════════════════════════════════════════════════════════════════════════════

@then("an order should be confirmed")
def order_is_confirmed(last_order: dict) -> None:
    from src.checkout import OrderStatus
    order = last_order["order"]
    assert order is not None, "No order was placed."
    assert order.status == OrderStatus.CONFIRMED, f"Expected CONFIRMED, got {order.status}"


@then(parsers.parse("the order total should be {expected:f}"))
def order_total(expected: float, last_order: dict) -> None:
    order = last_order["order"]
    assert order is not None, "No order was placed."
    assert order.total == pytest.approx(expected, abs=0.01), (
        f"Expected order total {expected}, got {order.total}"
    )


@then(parsers.parse('a checkout error should be raised with message "{fragment}"'))
def checkout_error_raised(fragment: str, checkout_error: dict) -> None:
    assert checkout_error["error"] is not None, "Expected a CheckoutError, but none was raised."
    assert fragment in str(checkout_error["error"]), (
        f"Expected error containing '{fragment}', got: '{checkout_error['error']}'"
    )
