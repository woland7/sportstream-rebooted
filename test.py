from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=DevToolsDisableDebugger"]
        )

        context = browser.new_context()
        page = context.new_page()

        # Optional: prevent popups


        # Open the streaming site
        page.goto("https://dlhd.dad/watch.php?id=56", wait_until="load")
        print("[✓] Page loaded.")

        # Inject script to remove overlays
        page.evaluate("""
            (() => {
                const removeOverlayAds = () => {
                    const elements = Array.from(document.querySelectorAll("body *"));
                    elements.forEach(el => {
                        const style = window.getComputedStyle(el);
                        const isOverlay = (
                            (style.position === "fixed" || style.position === "absolute") &&
                            (parseInt(style.zIndex || "0") > 100) &&
                            el.offsetWidth >= window.innerWidth * 0.9 &&
                            el.offsetHeight >= window.innerHeight * 0.9 &&
                            el !== document.body &&
                            el !== document.documentElement
                        );
                        if (isOverlay) {
                            el.remove();
                        }
                    });
                };

                // Initial cleanup
                removeOverlayAds();

                // Keep cleaning overlays every second
                setInterval(removeOverlayAds, 1000);
            })();
        """)
        print("[✓] Overlay removal script injected.")

        # Auto-click the fake play poster if it exists
        try:
            page.wait_for_selector(".player-poster.clickable", timeout=5000)
            page.click(".player-poster.clickable", timeout=3000)
            print("[✓] Clicked fake play button.")
        except:
            print("[!] No clickable poster found (may already be gone).")

        # Optionally auto-click real player play button
        try:
            page.wait_for_selector("video", timeout=5000)
            page.eval_on_selector("video", "el => el.play()")
            print("[✓] Video play triggered.")
        except:
            print("[!] Video not found or failed to play.")

        print("[🚀] Stream running. Your dad can now enjoy the show.")
        page.wait_for_timeout(60 * 60 * 1000)  # Keep open for 1 hour

if __name__ == "__main__":
    main()
