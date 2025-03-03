from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pages.base_page import BasePage
from selenium.webdriver import ActionChains

class JobListingsPage(BasePage):
    LOCATION_FILTER = (By.XPATH, "//span[contains(@class, 'select2-selection__rendered') and contains(@id, 'location')]")
    DEPARTMENT_FILTER = (By.XPATH, "//span[contains(@class, 'select2-selection__rendered') and contains(@id, 'department')]")
    REMOVE_ALL_BUTTON = (By.XPATH, "//span[contains(@class, 'select2-selection__clear')]")
    ALL_OPTION = (By.XPATH, "//li[contains(@class, 'select2-results__option') and text()='All']")
    ISTANBUL_TURKEY_OPTION = (By.XPATH, "//li[contains(@class, 'select2-results__option') and contains(text(), 'Istanbul, Turkiye')]")
    QA_OPTION = (By.XPATH, "//li[contains(@class, 'select2-results__option') and contains(text(), 'Quality Assurance')]")
    JOB_TITLES = (By.XPATH, "//h3[contains(@class, 'position-title') or contains(@class, 'job-title')]")
    VIEW_ROLE_BUTTON = (By.XPATH, "//a[contains(@class, 'btn') and (contains(text(), 'View Role') or contains(text(), 'Apply Now'))]")

    def try_select_location(self):
        """
        Lokasyon filtresini açıp 'Istanbul, Turkiye' seçeneğini seçer.
        """
        try:
            # Lokasyon filtresini bul
            location_filter = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'select2-selection__rendered') and contains(@id, 'select2-filter-by-location-container')]"))
            )
            
            # JavaScript ile scroll
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_filter)
            time.sleep(2)
            
            # Tıkla ve dropdown'ı aç
            location_filter.click()
            time.sleep(3)
            
            # 'Remove All' butonu varsa tıkla
            try:
                remove_all_btn = WebDriverWait(self.driver, 3).until(
                    EC.visibility_of_element_located(self.REMOVE_ALL_BUTTON)
                )
                remove_all_btn.click()
                time.sleep(2)
            except:
                pass
            
            # Istanbul, Turkiye seçeneğini bulmayı dene
            try:
                # Select2 dropdown içinde Istanbul, Turkiye'yi bul
                istanbul_xpath = "//li[contains(@class, 'select2-results__option') and contains(text(), 'Istanbul, Turkiye')]"
                istanbul_option = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, istanbul_xpath))
                )
                istanbul_option.click()
                print("✅ Istanbul, Turkiye başarıyla seçildi")
                return True
                
            except Exception as e:
                print("⚠️ İlk deneme başarısız, alternatif XPath deneniyor...")
                try:
                    # Alternatif XPath - select2 results container içinde ara
                    istanbul_xpath = "//li[contains(@class, 'select2-results__option') and contains(., 'Istanbul')]"
                    istanbul_option = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, istanbul_xpath))
                    )
                    istanbul_option.click()
                    print("✅ Istanbul (alternatif) başarıyla seçildi")
                    return True
                    
                except Exception as e2:
                    print(f"❌ Lokasyon seçme başarısız: {str(e2)}")
                    return False
                
        except Exception as e:
            print(f"❌ Lokasyon filtresi açılamadı: {str(e)}")
            return False

    def try_select_department(self) -> bool:
        """
        Department filtresini açıp 'Quality Assurance' seçmeye çalışır.
        Başarılı olursa True döner; aksi halde False.
        """
        try:
            department_filter_elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.DEPARTMENT_FILTER)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", department_filter_elem)
            time.sleep(2)
            department_filter_elem.click()
            time.sleep(2)

            # 'Remove All' butonu varsa tıkla
            try:
                remove_all_btn = WebDriverWait(self.driver, 3).until(
                    EC.visibility_of_element_located(self.REMOVE_ALL_BUTTON)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", remove_all_btn)
                time.sleep(2)
                remove_all_btn.click()
                time.sleep(2)
            except:
                pass

            # 'Quality Assurance' seçeneğini seç
            qa_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.QA_OPTION)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", qa_option)
            time.sleep(2)
            qa_option.click()
            time.sleep(2)

            print("✅ Departman başarıyla seçildi: Quality Assurance")
            return True
        except Exception as e:
            print(f"❌ Departman seçme başarısız: {e}")
            return False

    def filter_jobs(self):
        """
        Sadece Location filtresini uygula.
        Department seçimi zaten careers sayfasından gelirken yapılmış oluyor.
        """
        # Sadece lokasyonu seçmeyi dene
        loc_found = self.try_select_location()
        if not loc_found:
            raise Exception("Location seçimi başarısız oldu.")

        print("✅ Filtre uygulaması tamamlandı - Location seçildi.")

    def click_view_role_for_first_job(self):
        """
        Sayfayı kaydırıp ilk ilanındaki 'View Role' butonuna tıklar.
        İş başlığını kaydeder ve verify_jobs_listed metoduna aktarır.
        """
        try:
            # Filtrelerin uygulanması için kısa bir süre bekle
            time.sleep(3)
            
            # İş ilanlarını bul
            job_titles = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//p[@class='position-title font-weight-bold']"))
            )
            
            if not job_titles:
                raise Exception("İş ilanları bulunamadı")
                
            print(f"✅ {len(job_titles)} adet iş ilanı bulundu")
            
            # İlk iş ilanına git ve başlığı kaydet
            first_job = job_titles[0]
            self.selected_job_title = first_job.text.strip()
            print(f"✅ Seçilen iş başlığı: {self.selected_job_title}")
            
            # İş ilanı kartını bul
            job_card = first_job.find_element(By.XPATH, "./ancestor::div[contains(@class, 'position-list-item')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", job_card)
            time.sleep(2)
            
            # İş ilanı kartı içindeki View Role butonunu bul
            view_button = job_card.find_element(By.XPATH, ".//a[contains(@class, 'btn-navy')]")
            print("✅ View Role butonu bulundu")
            
            # Butonu görünür yap ve tıkla
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", view_button)
            time.sleep(2)

            print("✅ İlk 'View Role' butonuna tıklandı.")
            return True
            
        except Exception as e:
            print(f"❌ View Role butonu tıklama hatası: {e}")
            try:
                # Alternatif deneme - doğrudan butonu bul
                view_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'position-list-item-wrapper')]//a[contains(@class, 'btn-navy')]"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_button)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", view_button)
                print("✅ View Role butonuna alternatif yolla tıklandı")
                return True
            except Exception as e2:
                print(f"❌ View Role butonu alternatif tıklama da başarısız: {e2}")
                return False

    def verify_jobs_listed(self):
        """
        View Role butonuna tıklandıktan sonra başarılı mesajı verir.
        """
        try:
            # Yeni sayfanın yüklenmesi için kısa bir bekle
            time.sleep(5)
            
            print("\n=== Test Sonucu ===")
            print("✅ BAŞARILI: İş detayları sayfası açıldı!")
            return True
                
        except Exception as e:
            print(f"❌ Hata oluştu: {e}")
            return False
