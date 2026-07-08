import os
import re
import time
import logging


class BasePage:
    site_name = None

    def __init__(self, page):
        self.page = page
        self.logger = logging.getLogger(__name__)

    def open(self, url, goto_retries=3):
        """Navigate to `url` with a small retry loop to handle transient network interrupts."""
        for attempt in range(goto_retries):
            try:
                self.page.goto(url, timeout=60000, wait_until="domcontentloaded")
                try:
                    self.page.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    self.page.wait_for_timeout(3000)
                return
            except Exception as e:
                self.logger.warning(f"Navigation attempt {attempt + 1} failed for {url}: {e}")
                if attempt + 1 == goto_retries:
                    raise
                backoff = 3 * (2 ** attempt)
                self.logger.info(f"Retrying navigation in {backoff} seconds...")
                time.sleep(backoff)

    def screenshot_on_failure(self, url):
        safe_name = re.sub(r"[^\w]", "_", url)[:80]
        path = os.path.join("screenshots", f"{safe_name}.png")
        os.makedirs("screenshots", exist_ok=True)
        try:
            self.page.screenshot(path=path)
            return path
        except Exception:
            return None
