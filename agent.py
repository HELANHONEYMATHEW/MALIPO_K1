from playwright.sync_api import sync_playwright
from detector import detect_prompt_injection
from risk_engine import calculate_risk

class BrowserAgent:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

        # Track risks
        self.prompt_detected = False
        self.hidden_detected = False

    def open_page(self, url):
        print(f"[+] Opening: {url}")
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
        self.page.wait_for_timeout(2000)

    def scan_page(self):
        print("[+] Scanning page for prompt injection...")
        content = self.page.inner_text("body")

        detected, pattern = detect_prompt_injection(content)
        self.prompt_detected = detected

        if detected:
            print(f"[ALERT!!!] Prompt Injection Detected: '{pattern}'")
        else:
            print("===== No injection detected ======")

    def detect_hidden_elements(self):
        print("[+] Checking for hidden elements...")

        elements = self.page.query_selector_all("*")
        hidden_texts = []

        for el in elements:
            try:
                style = el.get_attribute("style")
                text = el.inner_text()

                # Skip empty or small text
                if not text or len(text.strip()) < 10:
                    continue

                # Skip CSS/JS-like content
                if "{" in text and "}" in text:
                    continue

                # Detect hidden styles
                if style and ("display:none" in style or "visibility:hidden" in style):
                    hidden_texts.append(text.strip())

            except:
                continue

        if hidden_texts:
            self.hidden_detected = True
            print("[ALERT!!!] Hidden suspicious content found:")
            for t in hidden_texts[:3]:
                print("   →", t)
        else:
            self.hidden_detected = False
            print("====== No hidden content detected =======")

    def safe_click(self, selector):
        print(f"[+] Attempting to click: {selector}")

        element = self.page.query_selector(selector)
        if not element:
            print("[X] Element not found")
            return

        try:
            text = element.inner_text()
        except:
            text = ""

        score, reasons = calculate_risk(
            self.prompt_detected,
            self.hidden_detected,
            text
        )

        print(f"[%%%%] Risk Score: {score}")

        if reasons:
            print("===== Reasons:")
            for r in reasons:
                print("   -", r)

        if score > 0.7:
            print("[BLOCKED] High-risk action prevented!")
            return
        elif score > 0.4:
            print("[WARNING] Medium risk — proceed carefully")

        print("==== Click allowed =====")
        element.click()


    def close(self):
        self.browser.close()
        self.playwright.stop()