Feature: DishAnyWhere home Promotions

  Scenario: DishAnyWhere Promotion List
    Given On DishAnyWhere Home page
    # like Web page get Most Pop and Promo List
    When Get Dish API Most and Promo Lists
    Then Dish Home Promotion List Matches API
