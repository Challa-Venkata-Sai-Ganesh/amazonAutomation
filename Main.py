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
    wait.until(
        expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR,
                                                                'div[class="puisg-col puisg-col-4-of-12 puisg-col-8-of-16 puisg-col-12-of-20 puisg-col-12-of-24 puis-list-col-right"]')))

    print("total cards present in page", len(total_cards))
    for item in total_cards:
        if remaining_products_extracted == 0:
            print("All products extracted")
            break
        else:
            data_extracted['card_title'].append(item.find_element(By.CSS_SELECTOR,
                                                                  "span[class='a-size-medium a-color-base a-text-normal']").text.strip())
            data_extracted['card_star_number'].append(
                item.find_element(By.CSS_SELECTOR, "span[class='a-size-base s-underline-text']").text.strip())
            data_extracted['card_current_price'].append(
                item.find_element(By.CSS_SELECTOR, 'span[class="a-price-whole"]').text.strip())
            data_extracted['card_mrp_price'].append(
                item.find_element(By.CSS_SELECTOR, "span[class='a-price a-text-price']").text.strip())
            remaining_products_extracted -= 1

    if remaining_products_extracted > 0:
        print("Moving to next Tab", remaining_products_extracted)
        driver.find_element(By.CSS_SELECTOR,
                            'a[class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').click()

        extract_details(driver, remaining_products_extracted, data_extracted)
    else:
        df = pd.DataFrame(data_extracted)
        df.to_csv("results.csv", index=False)


def verify(actual_result, expected_result):
    assert actual_result == expected_result


# def search_item_count(driver):
#     result_item = []
#     result_item = driver.find_element(
#         driver.find_element(By.CLASS_NAME, "a-section a-spacing-small a-spacing-top-small")).text.strip('')
#     print(result_item)

def run_selenium(search_item, brands_list, brand_data, rating, expected_results):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('headless')
    chrome_options.add_argument('--ignore-certificate-error')
    chrome_options.add_argument('--start-maximized')
    service_obj = Service()
    driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    driver.implicitly_wait(20)
    driver.get('https://www.amazon.in/')

    wait = WebDriverWait(driver, 15)
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
    wait = WebDriverWait(driver, 30)
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
            # 'card_rating': [],
            'card_star_number': [],
            'card_current_price': [],
            'card_mrp_price': []
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
