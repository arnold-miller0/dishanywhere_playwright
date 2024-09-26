Feature: DishAnyWhere home search example

  Scenario: DishAnyWhere copyright version
    Given On DishAnyWhere Home page
    Then Displays copyright and deployed version


  Scenario: DishAnyWhere search cbs
    Given On DishAnyWhere Home page
    When Search for cbs
    Then Finds CBS Sports Network
    Then Close Search

