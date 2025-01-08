# dishanywhere_playwright

Python version 3.12.4

## Requires to install 
- Given install python and pip
- pytest
  - `pip install pytest`
- pytest_bdd 
   - `pip install pytest_bdd`
- playwright python
  - `pip install --upgrade pip`
  - `pip install playwright`
  - `playwright install`

### TODO via similar typescript repo
- update locators to have tags not just via id, class, attributes
- Models and BDD tests check copyright and version via API response

## Checks DishAnyWhere home via Playwright python-pytest
- Footer's copyright **year and release version** via Config API
- Search finds specific network, shows, movies
- **Most Popular** carousel via its API response
- **Available Now** carousel via its API response
- **Promotion** carousel via API its response

## Tested via progress better style parts
- Part 1: Direct linear tests for Web and API
  - win11: `python -m pytest .\tests\part_1_direct\`
- Part 2: Use Web page, Web carousel and API Models
  - win11: `python -m pytest .\tests\part_2_models\`
- Part 3: BDD Feature Scenario using Part 2's Models
  - win11: `python -m pytest .\tests\part_3_bdd_normal\step_defs\`
- Part 4: BDD Feature Outline using Part 2' Models
  - win11: `python -m pytest .\tests\part_4_bdd_outline\step_defs\`

## DONE
