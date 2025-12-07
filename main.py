# Dropbox Automation Prototype using Playwright
# -----------------------------------------------------------
# This script demonstrates a working prototype for:
# 1. Logging into Dropbox
# 2. Navigating to the Admin page (if available)
# 3. Scraping the user list (names, emails)
# -----------------------------------------------------------
# IMPORTANT:
# - Replace EMAIL and PASSWORD with valid credentials
# - Dropbox may use MFA; this prototype handles login but not MFA
# - You can extend this for provisioning/deprovisioning

from playwright.sync_api import sync_playwright

DROPBOX_LOGIN_URL = "https://www.dropbox.com/login"
EMAIL = "sethshalini@hotmail.com"
PASSWORD = "Ang20@Rud24"


def login_and_scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Opening Dropbox login page...")
        page.goto(DROPBOX_LOGIN_URL)

        # Fill login form
        print("Filling login details...")
        page.fill("input[name='susi_email']", EMAIL)
        
        page.click("button[type='submit']")

        #page.wait_for_load_state("networkidle")
        page.fill("input[name='login_password']", PASSWORD)
        print("Logged in successfully.")

        # Navigate to Admin Console
        print("Navigating to Admin console...")
        page.goto("https://www.dropbox.com/team/admin/members")
        page.wait_for_load_state("networkidle")

        # Extract user table
        print("Extracting user list...")
        users = []

        rows = page.locator(".team-member-row").all()
        for row in rows:
            name = row.locator(".team-member-name").inner_text(timeout=1000)
            email = row.locator(".team-member-email").inner_text(timeout=1000)
            users.append({"name": name, "email": email})

        print("Users scraped:")
        print(users)

        browser.close()


if __name__ == "__main__":
    login_and_scrape()
