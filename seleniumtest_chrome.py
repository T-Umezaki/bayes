from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
from selenium.webdriver.chrome.options import Options
import codecs

# HTTP_PROXY = 'user:pass@http://192.168.236.23:8080'
# HTTPS_PROXY = 'user:pass@https://192.168.236.23:8080'
# PROXY_AUTH = 'user:pass'


class TestWebdriver(unittest.TestCase):
    def setUp(self):
        chromeOptions = Options()
        # chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument("--proxy-server=" + HTTP_PROXY)
        # chromeOptions.add_argument("--proxy-auth=" + PROXY_AUTH)
        self.driver = webdriver.Chrome('.\chromedriver', chrome_options=chromeOptions)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.yahoo.co.jp/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_webdriver(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        # 減っだページからリスト読み込み
        pages = driver.find_elements_by_xpath("//ul[@class='emphasis']/li/a")
        
        # encode でエラーが出るので、バイナリーで開く https://qiita.com/butada/items/33db39ced989c2ebf644
        file_results = codecs.open("./result_pages.txt", "a", "shift_jis", "ignore")
        # file_results = open("./result_pages.txt", "ab")
        print(len(pages))

        # リンク先から本文読み込み
        cnt_anker = 0
        for page in pages:
            pages2 = driver.find_elements_by_xpath("//ul[@class='emphasis']/li/a")
            pages2[cnt_anker].click()
            anker_test = driver.find_element_by_xpath("//div[@class='headlineTxt']/h2//a")
            title = anker_test.text
            # encoded_title = title.encode('cp932', "ignore")
            p_honbun = driver.find_element_by_xpath("//div[@class='headlineTxt']/p")
            honbun = p_honbun.text
            # encoded_honbun = honbun.encode('cp932', "ignore")
            # CSV作成
            file_results.write(title + "," + honbun + "\n")
            # 戻る
            driver.back()
            cnt_anker += 1
        driver.save_screenshot("screenshot.png")
        file_results.close()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException():
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException():
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()