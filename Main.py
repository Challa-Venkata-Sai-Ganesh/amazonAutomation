from time import sleep

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def verify(actual_result, expected_result):
    assert actual_result == expected_result


# def search_item_count(driver):
#     result_item = []
#     result_item = driver.find_element(
#         driver.find_element(By.CLASS_NAME, "a-section a-spacing-small a-spacing-top-small")).text.strip('')
#     print(result_item)


# # def item_Count():
def run_selenium(search_item, brands_list, brand_data, rating, expected_results):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('headless')
    chrome_options.add_argument('--ignore-certificate-error')
    chrome_options.add_argument('--start-maximized')
    service_obj = Service()
    driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    driver.implicitly_wait(10)
    driver.get('https://www.amazon.in/')
    # wait = WebDriverWait(driver, 10)
    # wait.until(expected_conditions.presence_of_element_located(
    #     (By.CSS_SELECTOR, 'a[class="nav-logo-link nav-progressive-attribute"]')))
    driver.find_element(By.ID, 'twotabsearchtextbox').send_keys(search_item)
    driver.find_element(By.ID, 'nav-search-submit-button').click()
    search_result = driver.find_element(By.CSS_SELECTOR, "span[class='a-color-state a-text-bold']").text.strip('""')
    verify(search_result, search_item)
    # all_products = []
    for key in brands_list:  # [1, 3]
        brand_name = brand_data[key]  # brand_data[1]

        driver.find_element(By.XPATH, f"// *[ @ id = 'p_89/{ brand_name}'] / span / a / span").click()

        # wait = WebDriverWait(driver, 15)
        # # # clicking brand names
        # wait.until(expected_conditions.presence_of_element_located(
        #     (By.CSS_SELECTOR, "span[class='a-size-medium a-color-base']")))
        # all_products = driver.find_elements(By.CSS_SELECTOR, "span[class='a-size-medium a-color-base']")

    if rating == '4':
        driver.find_element(By.CSS_SELECTOR, "span[data-csa-c-content-id='p_72/1318476031']").click()
    else:
        pass
    sleep(10)
    search_results = driver.find_element(By.XPATH,
                                               '//*[@id="search"]/span[2]/div/h1/div/div[1]/div/div/span[1]').text.split(' ')

    total_results = int(search_results[2])
    print(total_results)
    count = 0
    if total_results == 0:
        print("no results found")
    else:
        card_title = []
        card_rating = []
        card_star_count = []
        while count <= expected_results:
            driver.find_element(By.CSS_SELECTOR,
                                'h2[class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]').text
            count += 1




    # PAGE MAIN LOADING PROBLEM


if __name__ == "__main__":
    search_term = str(input("Please enter the name of the product you wish to search on amazon: ")).capitalize()
    print(f"you have chosen {search_term}")
    print(f"Below are the list of {search_term} brands we help you with:")
    laptop_brands = {
        1: 'Dell',
        2: 'Lenovo',
        3: 'ASUS'
    }
    mobile_brands = {
        1: 'Oppo',
        2: 'One Plus',
        3: 'Apple'
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
    rating_input = input("Enter the star rating from above number : ")
    expected_results = int(input("Please enter nearer expected results"))

    run_selenium(search_term, brand_input_list, laptop_brands, rating_input, expected_results)
