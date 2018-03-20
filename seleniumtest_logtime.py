#!/usr/bin/python3

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import sys

# chromedriver.exe を同一フォルダに格納してください。git内にあります。
# 実行コマンド python seleniumtest_logtime.py s ←出勤。 退勤は t
# 社内向け。Proxy突破の実装はありません


class TestWebdriver(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('.\chromedriver')
        self.driver.implicitly_wait(30)
        self.base_url = "https://ltap.sis.saison.co.jp/logtime/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_webdriver(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        print(driver.title)
        element = driver.find_element_by_name("username")
        element.send_keys("1013387")
        element = driver.find_element_by_name("password")
        element.send_keys("lt1013387")
        driver.find_element_by_xpath('//*[@id="loginButton"]/table/tbody/tr[5]/td/a').click()
        # ページ遷移
        # 対象Frameに遷移：はまったT T
        driver.switch_to.frame("frameMain")
        driver.switch_to.frame(0)
        if sys.argv[1] == "t":
            element = driver.find_element_by_xpath('//a[@class="topTaikinDakoku"]')
        else:
            element = driver.find_element_by_xpath('//a[@class="topShukkinDakoku"]')
        element.click()
        driver.save_screenshot("screenshot.png")

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
    # 引数： s:出勤 t:退勤 なし:エラー
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
