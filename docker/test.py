from playwright.sync_api import sync_playwright

def main():
    print("Test script is running!")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            executable_path="/usr/bin/google-chrome-stable",  # real Chrome
            args=["--no-sandbox"]
        )
        context = browser.new_context()

        # Override `performance.now` to neutralize timing detection
        context.add_init_script("""
            const originalNow = performance.now;
            performance.now = () => originalNow() - 200;

            // Overwrite the debugger function
            const originalDebug = window.debugger;
            window.debugger = function () {};
        """)

        page = context.new_page()
        page.goto("https://dlhd.dad/watch.php?id=56", wait_until="load")
        print("Bypassed DevTools detection.")

        # Keep browser open
        page.wait_for_timeout(1000 * 60 * 60)  # 1 hour

if __name__ == "__main__":
    main()
