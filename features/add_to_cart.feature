# features/add_to_cart.feature

Feature: Add items to shopping cart
  As a shopper
  I want to add products to my cart
  So that I can purchase them later

  Background:
    Given a user "alice" has an empty shopping cart

  Scenario: Add a single in-stock product
    Given a product "Wireless Headphones" priced at 2999.00 with 10 in stock
    When the user adds 1 "Wireless Headphones" to the cart
    Then the cart should contain 1 item
    And the cart subtotal should be 2999.00

  Scenario: Add multiple different products
    Given a product "Wireless Headphones" priced at 2999.00 with 10 in stock
    And a product "Phone Case" priced at 299.00 with 50 in stock
    When the user adds 1 "Wireless Headphones" to the cart
    And the user adds 2 "Phone Case" to the cart
    Then the cart should contain 3 items
    And the cart subtotal should be 3597.00

  Scenario: Add more than available stock raises an error
    Given a product "Limited Edition Watch" priced at 15000.00 with 2 in stock
    When the user tries to add 5 "Limited Edition Watch" to the cart
    Then a cart error should be raised with message "Only 2 unit(s)"

  Scenario: Add an out-of-stock product raises an error
    Given a product "Sold-Out Sneakers" priced at 4500.00 with 0 in stock
    When the user tries to add 1 "Sold-Out Sneakers" to the cart
    Then a cart error should be raised with message "out of stock"

  Scenario Outline: Add various quantities of a product
    Given a product "USB Hub" priced at 799.00 with 20 in stock
    When the user adds <qty> "USB Hub" to the cart
    Then the cart subtotal should be <expected_total>

    Examples:
      | qty | expected_total |
      | 1   | 799.00         |
      | 3   | 2397.00        |
      | 5   | 3995.00        |
