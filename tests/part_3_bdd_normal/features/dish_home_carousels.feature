Feature: DishAnyWhere home Carousels

  Scenario: DishAnyWhere Avail Now Carousel
    Given On DishAnyWhere Home page
    When Get Dish API Avail Now List
    Then Dish Home Avail Now List has Title
    Then Dish Home Avail Now List Matches API


  Scenario: DishAnyWhere Most Popular Carousel
    Given On DishAnyWhere Home page
    When Get Dish API Most Popular List
    Then Dish Home Most Popular List has Title
    Then Dish Home Most Popular List Matches API