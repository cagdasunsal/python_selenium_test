from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage

class HomePage(BasePage):
    URL = "https://useinsider.com/"
    COMPANY_MENU = (By.XPATH, "//a[contains(text(), 'Company')]")
    CAREERS_LINK = (By.XPATH, "//a[contains(text(), 'Careers')]")

    def wait_for_page_load(self):
        """Sayfanın tamamen yüklendiğinden emin ol."""
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print("✅ Sayfa tamamen yüklendi.")
        except Exception as e:
            print(f"⚠️ Sayfa yükleme hatası: {e}")

    def open_home_page(self):
        self.driver.get(self.URL)

    def go_to_careers_page(self):
        self.click(self.COMPANY_MENU)
        self.click(self.CAREERS_LINK)
