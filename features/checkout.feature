# features/checkout.feature

Feature: Checkout and place an order
  As a shopper who has items in my cart
  I want to place an order with my delivery address and payment method
  So that I can receive the products at my door

  Background:
    Given a user "dave" has an empty shopping cart
    And a product "Mechanical Keyboard" priced at 5500.00 with 8 in stock
    And a product "Monitor" priced at 18000.00 with 5 in stock
    And the user adds 1 "Mechanical Keyboard" to the cart
    And a checkout service is ready

  Scenario: Successfully place an order with UPI payment
    Given a valid delivery address for "Dave Kumar" in "Mumbai" with pincode "400001"
    When the user checks out using "upi"
    Then an order should be confirmed
    And the order total should be 5500.00
    And the cart should be empty

  Scenario: Place an order with a coupon applied
    Given a product "USB Hub" priced at 1200.00 with 20 in stock
    And the user adds 1 "USB Hub" to the cart
    And a coupon "FLAT10" offering 10% off with minimum order 5000.00
    And the user applies coupon "FLAT10"
    And a valid delivery address for "Dave Kumar" in "Pune" with pincode "411001"
    When the user checks out using "credit_card"
    Then an order should be confirmed
    And the order total should be 6030.00

  Scenario: Cannot check out with an empty cart
    Given a user "empty_user" has an empty shopping cart
    And a valid delivery address for "Empty User" in "Delhi" with pincode "110001"
    When the user tries to check out using "upi"
    Then a checkout error should be raised with message "empty cart"

  Scenario: COD is blocked for orders above Rs 50000
    Given the user adds 3 "Monitor" to the cart
    And a valid delivery address for "Dave Kumar" in "Bangalore" with pincode "560001"
    When the user tries to check out using "cod"
    Then a checkout error should be raised with message "COD not available"

  Scenario: Invalid pincode blocks checkout
    Given a delivery address with invalid pincode "ABC123"
    When the user tries to check out using "upi"
    Then a checkout error should be raised with message "Invalid pincode"
