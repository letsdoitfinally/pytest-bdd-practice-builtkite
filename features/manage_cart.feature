# features/manage_cart.feature

Feature: Manage cart items
  As a shopper
  I want to update or remove items in my cart
  So that I can adjust my order before checkout

  Background:
    Given a user "carol" has an empty shopping cart
    And a product "Keyboard" priced at 1200.00 with 15 in stock
    And a product "Mouse" priced at 600.00 with 10 in stock
    And the user adds 2 "Keyboard" to the cart
    And the user adds 1 "Mouse" to the cart

  Scenario: Remove an item from the cart
    When the user removes "Keyboard" from the cart
    Then the cart should contain 1 item
    And the cart subtotal should be 600.00

  Scenario: Update quantity of an existing item
    When the user updates "Keyboard" quantity to 1
    Then the cart should contain 2 items
    And the cart subtotal should be 1800.00

  Scenario: Setting quantity to zero removes the item
    When the user updates "Mouse" quantity to 0
    Then the cart should contain 2 items
    And the cart does not contain "Mouse"

  Scenario: Clear the entire cart
    When the user clears the cart
    Then the cart should be empty
