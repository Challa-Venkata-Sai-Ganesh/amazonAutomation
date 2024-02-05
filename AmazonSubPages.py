import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd


def extract_details(driver, remaining_products_extracted, data_extracted):
    time.sleep(2)
    total_cards = driver.find_elements(By.CSS_SELECTOR,
                                       'div[class="puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right"]')

    wait = WebDriverWait(driver, 15)
    wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                                                       'div[class="puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right"]')))

    print("total cards present in page", len(total_cards))
    for item in total_cards:
        if remaining_products_extracted == 0:
            print("All products extracted")
            break
        else:
            item.find_element(By.CSS_SELECTOR, "span[class='a-size-medium a-color-base a-text-normal']").click()
            windows_opened = driver.window_handles
            driver.switch_to.window(windows_opened[1])
            wait = WebDriverWait(driver, 15)
            wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div[id='centerCol'] div h1 span[id='productTitle']")))
            data_extracted['card_title'].append(driver.find_element(By.CSS_SELECTOR, "div[id='centerCol'] div h1 span[id='productTitle']").text.strip())
            data_extracted['card_rating'].append(driver.find_element(By.CSS_SELECTOR, "div[id='centerCol'] div div span span span a span[class='a-size-base a-color-base']").text.strip())
            #
            data_extracted['card_avg_reviews'].append(driver.find_element(By.CSS_SELECTOR, "div[id='centerCol'] div div span a span[id='acrCustomerReviewText']").text.replace('ratings', '').strip())
            data_extracted['card_current_price'].append(driver.find_element(By.CSS_SELECTOR, "div[id='centerCol'] div div div div div span span[class='a-price-whole']").text.strip())
            data_extracted['card_mrp_price'].append(driver.find_element(By.CSS_SELECTOR, "div[id='centerCol'] div div div div div span span span span[class='a-offscreen']").text.strip())

            driver.find_element(By.XPATH, '//*[@id="poToggleButton"]/a/span').click()
            wait = WebDriverWait(driver, 20)
            wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[10]/td[2]/span[@class="a-size-base po-break-word"]')))
            data_extracted['card_brand'].append(driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[1]/td[2]/span[@class="a-size-base po-break-word"]').text.strip())
            data_extracted['card_model_name'].append(driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[2]/td[2]/span[@class="a-size-base po-break-word"]').text.strip())
            data_extracted['card_screen_size'].append(driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[3]/td[2]/span[@class="a-size-base po-break-word"]').text.strip())
            data_extracted['card_colour'].append(driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[4]/td[2]/span[@class="a-size-base po-break-word"]').text.strip())
            data_extracted['card_harddisk_size'].append(driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[5]/td[2]/span[@class="a-size-base po-break-word"]').text.strip())
            data_extracted['card_cpu_model'].append(driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[6]/td[2]/span[@class="a-size-base po-break-word"]').text.strip())
            data_extracted['card_ram'].append(driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[7]/td[2]/span[@class="a-size-base po-break-word"]').text.strip())
            # data_extracted['card_os'].append(driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[8]/td[2]/span[@class="a-size-base po-break-word"]').text.strip())
            # data_extracted['card_special_feature'].append(driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[9]/td[2]/span[@class="a-size-base po-break-word"]').text.strip())
            data_extracted['card_graphic_card'].append(driver.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]/tbody//tr[10]/td[2]/span[@class="a-size-base po-break-word"]').text.strip())

            try:
                wait = WebDriverWait(driver, 5)
                wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//p[@class="a-spacing-small"]/span')))
                data_extracted['card_customer_say'].append(driver.find_element(By.XPATH, '//p[@class="a-spacing-small"]/span').text.strip())
            except Exception as e:
                customer_say = 'n/a'
                data_extracted['card_customer_say'].append(customer_say)

            driver.close()
            driver.switch_to.window(windows_opened[0])
            remaining_products_extracted -= 1

    if remaining_products_extracted > 0:
        page_count = 1
        print("remaining products : ", remaining_products_extracted)
        driver.find_element(By.CSS_SELECTOR,
                            'a[class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').click()
        page_count += 1
        print("current page : ", page_count)
        time.sleep(2)
        extract_details(driver, remaining_products_extracted, data_extracted)
    else:
        df = pd.DataFrame(data_extracted)
        df.to_csv("results_subpages.csv", index=False)


def verify(actual_result, expected_result):
    assert actual_result == expected_result


def run_selenium(search_item, brands_list, brand_data, rating, expected_results):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('headless')
    chrome_options.add_argument('--ignore-certificate-error')
    chrome_options.add_argument('--start-maximized')
    service_obj = Service()
    driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    driver.implicitly_wait(20)
    driver.get('https://www.amazon.in/')

    wait = WebDriverWait(driver, 20)
    wait.until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, 'a[class="nav-logo-link nav-progressive-attribute"]')))
    driver.find_element(By.ID, 'twotabsearchtextbox').send_keys(search_item)
    driver.find_element(By.ID, 'nav-search-submit-button').click()
    search_result = driver.find_element(By.CSS_SELECTOR, "span[class='a-color-state a-text-bold']").text.strip('""')
    verify(search_result, search_item)

    for key in brands_list:  # [1, 3]
        brand_name = brand_data[key]  # brand_data[1]
        driver.find_element(By.XPATH, f"// *[ @ id = 'p_89/{brand_name}'] / span / a / span").click()

    if rating == 4:
        driver.find_element(By.CSS_SELECTOR, "span[data-csa-c-content-id='p_72/1318476031']").click()
        time.sleep(3)
    elif rating == 0:
        pass
    wait = WebDriverWait(driver, 40)
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH,
                                                                  '//*[@id="search"]/span[2]/div/h1/div/div[1]/div/div/span[1]')))

    search_results = driver.find_element(By.XPATH,
                                         '//*[@id="search"]/span[2]/div/h1/div/div[1]/div/div/span[1]').text.split()

    total_results = int(search_results[2])
    print("Total Search results : {} ".format(total_results))

    if total_results > 0:
        print("Entered IF")
        data_extracted = {
            'card_title': [],
            'card_rating': [],
            'card_avg_reviews': [],
            'card_current_price': [],
            'card_mrp_price': [],
            'card_brand': [],
            'card_model_name': [],
            'card_screen_size': [],
            'card_colour': [],
            'card_harddisk_size': [],
            'card_cpu_model': [],
            'card_ram': [],
            # 'card_os': [],
            # 'card_special_feature': [],
            'card_graphic_card': [],
            'card_customer_say': []

        }

        remaining_products_extracted = expected_results  # 35

        extract_details(driver, remaining_products_extracted, data_extracted)


if __name__ == "__main__":
    search_term = str(input("Please enter the name of the product you wish to search on amazon: ")).capitalize()
    print(f"you have chosen {search_term}.Below are the list of {search_term} brands we help you with:")
    laptop_brands = {
        1: 'Dell',
        2: 'Lenovo',
        3: 'ASUS'
    }
    mobile_brands = {
        1: 'Samsung',
        2: 'OnePlus',
        3: 'POCO'
    }

    customer_rating = {
        4: '4',
        0: 'no selection'
    }
    if search_term == "Laptop":
        print(laptop_brands)
    elif search_term == "Mobiles":
        print(mobile_brands)

    brand_input = str(input("Choose multiple brands with brand number. please provide space separated numbers:"))
    brand_input_list = list(map(int, brand_input.split()))
    print("You have chosen brand names:", brand_input_list)
    print(customer_rating)
    rating_input = int(input("Enter the star rating from above number : "))
    expected_results = int(input("Please enter nearer expected results : "))

    run_selenium(search_term, brand_input_list, laptop_brands, rating_input, expected_results)
