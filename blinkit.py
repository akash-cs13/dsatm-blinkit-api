from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os

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

    def set_location(self, pincode = '560004'):
        #area = self.find_element(by=By.CSS_SELECTOR, value='input[data-test-id="area-input-box"]')
        area = WebDriverWait(self, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-test-id="area-input-box"]')))

        area.send_keys("Thayagaraja")
        sleep(2)
        area.send_keys("Nagar")
        sleep(3)
        area.send_keys(Keys.ARROW_DOWN, Keys.ENTER)



    def search_for_product(self, product):
        self.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Search for products"]').send_keys(
            Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE,
            Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE,
            Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE,
            Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE,
            Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE)
        sleep(1)
        self.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Search for products"]').send_keys(product, Keys.ENTER)
        sleep(2)

        items = self.find_elements(by=By.CLASS_NAME, value="Product__ProductName-sc-11dk8zk-4")
        packet_desc = self.find_elements(by=By.CLASS_NAME, value="plp-product__quantity--box")
        price = self.find_elements(by=By.CLASS_NAME, value="ProductPrice__Price-sc-14194u2-1")
        #url = self.find_elements(by=By.CSS_SELECTOR, value='a[class ="product__wrapper"  data-test-id="plp-product"]')
        url = self.find_elements(by=By.CLASS_NAME, value="product__wrapper")
        img = self.find_elements(by=By.CLASS_NAME, value="sc-iBkjds")


        #img = self.find_elements(by=By.CSS_SELECTOR, value='img[class="img-loader__img--plp"]')
        #WebDriverWait(self, 5).until(EC.visibility_of_all_elements_located(img))

        return_list = []
        for i in range(0, len(items)):
            return_list.append((items[i].text, packet_desc[i].text, price[i].text[1:], url[i].get_attribute("href"), img[i].get_attribute("src")))
            #img[i].get_attribute("src")
            #return_list.append((items[i].text, packet_desc[i].text, price[i].text[1:], url[i].get_attribute("href")))




        return return_list

if __name__ == '__main__':
    inst = Blinkit_api()
    print("Initializing api.................................")
    inst.initialization()
    print("Setting up location.....................")
    inst.set_location()
    print("Initialization is done!!!!!!!!!\n")

    labels = ['Apple', 'Banana', 'Coconut', 'Curd', 'Guava', 'Mango', 'Milk', 'Mosambi', 'Muskmelon', 'Onion', 'Orange', 'Papaya', 'Pomegranate', 'Potato', 'Tomato']
    #labels = ['Apple', 'Onion', 'Potato']

    json_write = {}

    for read_string in labels:
        product_list = inst.search_for_product(read_string)
        print("Fetching data for "+ read_string)

        temp_list = []
        for item, packet_desc, price, url, img in product_list:
            temp_list.append({"item": item, "packet_description": packet_desc, "price": price, "url": url, "img": img})


        json_write[read_string] = temp_list
        print('\n')


    inst.quit()
    f = open("Blinkitapi.json", "w")
    f.write(json.dumps(json_write))
    f.close()




