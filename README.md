# dishanywhere_playwright


### TODO via similar typescript repo
- update locators to have tags not just via id, class, attributes
- Models and BDD tests check copyright and version via API response

**Python version 3.12.4**
## Requires to install 
### Given installed python and pip
- `python 3.12.4`
- `pip 24.3.1`
### upgrade pip
- `pip install --upgrade pip`
### install pytest
- `pip install pytest`
### install pytest-html
- `pip install pytest-html`
### install pytest_bdd 
- `pip install pytest_bdd`
### install playwright
- `pip install playwright`
- `playwright install`


## Checks DishAnyWhere home via Playwright python-pytest
- Footer's copyright **year and release version** via Config API
- Search finds specific network, shows, movies
- **Most Popular** carousel via its API response
- **Available Now** carousel via its API response
- **Promotion** carousel via API its response

## Tested via progress better style parts
- Part 1: Direct linear tests for Web and API
  - winOS11: `python -m pytest .\tests\part_1_direct\`
     - html: `python -m pytest .\tests\part_1_direct\ --html=reports/part_1_report.html  `
- Part 2: Use Web page, Web carousel and API Models
  - winOS11: `python -m pytest .\tests\part_2_models\`
     - html: `python -m pytest .\tests\part_2_models\ --html=reports/part_2_report.html`
- Part 3: BDD Feature Scenario using Part 2's Models
  - winOS11: `python -m pytest .\tests\part_3_bdd_normal\step_defs\`
     - html: `python -m pytest .\tests\part_3_bdd_normal\ --html=reports/part_3_report.html`
- Part 4: BDD Feature Outline using Part 2' Models
  - winOS11: `python -m pytest .\tests\part_4_bdd_outline\step_defs\`
     - html: `python -m pytest .\tests\part_4_bdd_outline\ --html=reports/part_4_report.html`

## DONE
