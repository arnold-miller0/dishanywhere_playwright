from playwright.sync_api import sync_playwright, expect

def test_dish_title():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.dishanywhere.com/")
        print(f" DishAnywhere Title={page.title()};")
        expect(page).to_have_title("DISH Anywhere")
        browser.close()
