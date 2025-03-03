from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
import  time

class CareersPage(BasePage):
    CAREER_PAGE_HEADER = (By.TAG_NAME, "h1")
    SEE_ALL_TEAMS_BUTTON = (By.XPATH, "//a[contains(@class, 'loadmore') and contains(text(), 'See all teams')]")
    QUALITY_ASSURANCE_SECTION = (By.XPATH, "//h3[contains(text(), 'Quality Assurance')]")
    SEE_ALL_QA_JOBS_BUTTON = (By.XPATH, "//a[contains(text(), 'See all QA jobs')]")

    def verify_careers_page_loaded(self):
        """Sayfanın tamamen yüklenmesini bekler ve başlığı döndürür."""
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.SEE_ALL_TEAMS_BUTTON))
        return self.get_text(self.CAREER_PAGE_HEADER)

    def click_see_all_teams(self):
        """Sayfayı tamamen aşağı kaydır ve 'See All Teams' butonuna tıkla."""
        element = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.SEE_ALL_TEAMS_BUTTON))

        # 5 defa küçük kaydırmalar yaparak sayfayı aşağı indir
        for _ in range(5):
            self.driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(1)  # Kaydırmanın etkili olması için beklet

        # Butonu görünür hale getir
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

        # JavaScript ile butona tıkla
        self.driver.execute_script("arguments[0].click();", element)

    def select_quality_assurance(self):
        """'Quality Assurance' başlığının tıklanabilir olmasını bekler ve tıklar."""
        element = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.QUALITY_ASSURANCE_SECTION))

        # Sayfanın en altına kaydır (bazı öğeler yüklenmemiş olabilir)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        # Sayfayı tekrar yukarı kaydırarak QA başlığını görünür hale getir
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(2)

        # Elementi JavaScript ile tıklamak yerine Selenium’un ActionChains kullanarak tıklamasını sağla
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

    def click_see_all_qa_jobs(self):
        """'See All QA Jobs' butonuna tıklamak için sayfanın tamamen yüklendiğinden emin ol."""
        element = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.SEE_ALL_QA_JOBS_BUTTON))

        # Sayfanın tamamen yüklenmesini bekle
        time.sleep(2)

        # Sayfanın ortasına kaydır
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(2)



        # JavaScript ile doğrudan butona tıkla
        self.driver.execute_script("arguments[0].click();", element)
