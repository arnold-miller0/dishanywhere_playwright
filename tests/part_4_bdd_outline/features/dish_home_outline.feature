Feature: DishAnyWhere home outlines


  Scenario: Scenario: DishAnyWhere copyright version
    Given On DishAnyWhere Home size "1280" x "960"
    Then Displays copyright "2024" and version "24.3.5"


  Scenario Outline: DishAnyWhere Search networks
    Given On DishAnyWhere Home page
    When Search for "<item>"
    Then Finds id "<id_attr>" with "<text>"
    Then Close Search
    Examples:
      | item | id_attr                             | text               |
      | cbS  | cbs_sports_network_1220-search-link | CBS Sports Network |
      | Pbs  | pbs_kids_1006-search-link           | PBS Kids           |
      | nbC  | dateline_nbc_e24749-search-link     | Dateline NBC       |


  Scenario Outline: DishAnyWhere Home Lists
    Given On DishAnyWhere Home size "<width>" x "<height>"
    When Get Dish API "<name>" List
    Then Dish Home "<name>" List has Title
    Then Dish Home "<name>" List Matches API
    Examples:
      | name      | width | height | comment
      | other     | 1800  | 700    | not found Carousel
      | avail now | 1700  | 800    | Available Now Carousel
      | most pop  | 1600  | 900    | Moet Popular Carousel
      | promos    | 1500  | 1000   | Promotional List
