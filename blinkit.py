import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Blinkit_api(webdriver.Chrome):
    def __init__(self):
        chrome_options = Options()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.headless = True
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        super(Blinkit_api, self).__init__(service=Service(os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)
        super(Blinkit_api, self).__init__(options=chrome_options)
        self.implicitly_wait(20)

    def initialization(self):
        self.get('https://www.blinkit.com')

    def exit(self):
        self.quit()

    def set_location(self, pincode = '560028'):
        sleep(3)
        self.find_element(by=By.CSS_SELECTOR, value='input[data-test-id="area-input-box"]').send_keys(pincode)
        sleep(3)
        self.find_element(by=By.CSS_SELECTOR, value='input[data-test-id="area-input-box"]').send_keys(Keys.ARROW_DOWN, Keys.ENTER)

    def search_for_product(self, product):
        self.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Search for products"]').send_keys(product, Keys.ENTER)

        items = self.find_elements(by=By.CLASS_NAME, value="plp-product__name--box")
        packet_desc = self.find_elements(by=By.CLASS_NAME, value="plp-product__quantity--box")
        price = self.find_elements(by=By.CLASS_NAME, value="plp-product__price--new")
        url = self.find_elements(by=By.CLASS_NAME, value="product__wrapper")

        return_list = []
        for i in range(0, len(items)):
            return_list.append((items[i].text, packet_desc[i].text, price[i].text[1:], url[i].get_attribute("href")))


        return return_list

if __name__ == '__main__':
    inst = Blinkit_api()
    print("Initializing api.................................")
    inst.initialization()
    print("Setting up location.....................")
    inst.set_location()
    print("Initialization is done!")

    while True:
        read_string = input("\nEnter 'quit' if you want to exit \nSearch: ")

        if read_string == "quit": break

        product_list = inst.search_for_product(read_string)
        for tup in product_list:
            print(tup)
        print("\n\n\n")

    inst.quit()




