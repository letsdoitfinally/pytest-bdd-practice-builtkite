# features/coupon_discount.feature

Feature: Apply discount coupons
  As a shopper
  I want to apply coupon codes at checkout
  So that I get a discount on my order

  Background:
    Given a user "bob" has an empty shopping cart
    And a product "Laptop Stand" priced at 1500.00 with 30 in stock
    And the user adds 2 "Laptop Stand" to the cart

  Scenario: Apply a valid 10% coupon
    Given a coupon "SAVE10" offering 10% off with minimum order 500.00
    When the user applies coupon "SAVE10"
    Then the discount amount should be 300.00
    And the cart total should be 2700.00

  Scenario: Apply a coupon below minimum order value raises an error
    Given a coupon "BIG50" offering 50% off with minimum order 5000.00
    When the user tries to apply coupon "BIG50"
    Then a cart error should be raised with message "Minimum order"

  Scenario: Apply an inactive coupon raises an error
    Given an inactive coupon "EXPIRED20"
    When the user tries to apply coupon "EXPIRED20"
    Then a cart error should be raised with message "inactive"

  Scenario: Cart total equals subtotal when no coupon applied
    Then the discount amount should be 0.00
    And the cart total should be 3000.00
