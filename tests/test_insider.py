import pytest
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.job_listings_page import JobListingsPage
import time
 # Sayfanın yüklenmesini beklet


def test_insider_career_page(browser):

    home_page = HomePage(browser)
    careers_page = CareersPage(browser)
    jobs_page = JobListingsPage(browser)
    home_page.wait_for_page_load()


    # 1. Insider ana sayfasını aç
    home_page.open_home_page()
    time.sleep(3)

    # 2. "Careers" sayfasına git ve açıldığını doğrula
    home_page.go_to_careers_page()
    assert "Ready to disrupt" in careers_page.verify_careers_page_loaded()


    # 3. "See All Teams" butonuna tıkla
    careers_page.click_see_all_teams()

    # 4. "Quality Assurance" başlığını bul ve tıkla
    careers_page.select_quality_assurance()

    # 5. "See All QA Jobs" butonuna tıkla
    careers_page.click_see_all_qa_jobs()

    # 6. QA iş ilanlarını filtrele
    jobs_page.filter_jobs()
    jobs_page.click_view_role_for_first_job()

    # 7. İş ilanlarının doğru olduğunu doğrula
    assert jobs_page.verify_jobs_listed()
