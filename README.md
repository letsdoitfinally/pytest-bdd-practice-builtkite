# pytest-BDD Framework — E-Commerce Shopping Cart

A **real-life BDD (Behaviour-Driven Development)** test framework built with
[pytest-bdd](https://pytest-bdd.readthedocs.io/) demonstrating how teams write
tests that non-technical stakeholders can read and validate.

---

## Project Structure

```
pytest_bdd_demo/
│
├── features/                        # ← Gherkin feature files (plain English)
│   ├── add_to_cart.feature
│   ├── coupon_discount.feature
│   ├── manage_cart.feature
│   └── checkout.feature
│
├── src/                             # ← Business logic (no pytest dependency)
│   ├── cart.py                      #   ShoppingCart, Product, Coupon, CartItem
│   └── checkout.py                  #   CheckoutService, Order, Address
│
├── tests/
│   ├── conftest.py                  # ← Shared fixtures + ALL step definitions
│   └── step_defs/
│       ├── test_add_to_cart.py      # ← scenarios("add_to_cart.feature")
│       ├── test_coupon_discount.py
│       ├── test_manage_cart.py
│       └── test_checkout.py        # ← checkout-specific steps here
│
├── conftest.py                      # ← Root hooks: logging, reporting
├── pytest.ini                       # ← pytest config (bdd_features_base_dir)
└── requirements.txt
```

---

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
# All tests
pytest

# A single feature
pytest tests/step_defs/test_checkout.py -v

# By marker
pytest -m smoke -v

# With step-by-step logging
pytest -s -v

# HTML report
pytest --html=reports/report.html --self-contained-html
```

---

## Key Concepts

### 1. Gherkin Syntax
```gherkin
Feature: Add items to shopping cart

  Background:
    Given a user "alice" has an empty shopping cart   # runs before EVERY scenario

  Scenario: Add a single in-stock product
    Given a product "Headphones" priced at 2999.00 with 10 in stock
    When the user adds 1 "Headphones" to the cart
    Then the cart should contain 1 item               # assert
    And the cart subtotal should be 2999.00

  Scenario Outline: Various quantities
    Given a product "USB Hub" priced at 799.00 with 20 in stock
    When the user adds <qty> "USB Hub" to the cart
    Then the cart subtotal should be <expected_total>

    Examples:                                          # generates 3 test cases
      | qty | expected_total |
      | 1   | 799.00         |
      | 3   | 2397.00        |
      | 5   | 3995.00        |
```

### 2. Step Definitions
```python
from pytest_bdd import given, when, then, parsers

@given(parsers.parse('a product "{name}" priced at {price:f} with {stock:d} in stock'))
def a_product_exists(name, price, stock, product_registry):
    product_registry[name] = Product(id=name, name=name, price=price, stock=stock)

@when(parsers.parse('the user adds {qty:d} "{name}" to the cart'))
def user_adds_item(qty, name, cart, product_registry):
    cart.add_item(product_registry[name], quantity=qty)

@then(parsers.parse("the cart subtotal should be {expected:f}"))
def cart_subtotal(expected, cart):
    assert cart.subtotal == pytest.approx(expected, abs=0.01)
```

### 3. Parsers
| Parser | Use when |
|--------|----------|
| `parsers.parse(...)` | Simple typed tokens: `{name}`, `{qty:d}`, `{price:f}` |
| `parsers.re(r"...")` | Complex patterns, special chars (`%`, `$`), optional groups |
| `parsers.cfparse(...)` | Same as parse but with cardinality (`{items:w+}`) |

### 4. `target_fixture`
`Given` steps can return a value that becomes a pytest fixture:
```python
@given("a checkout service is ready", target_fixture="checkout_service")
def a_checkout_service():
    return CheckoutService()   # injected into subsequent steps
```

---

## Test Results
```
20 passed in 0.06s
├── add_to_cart    — 7 tests (incl. 3 Scenario Outline rows)
├── checkout       — 5 tests
├── coupon         — 4 tests
└── manage_cart    — 4 tests
```
