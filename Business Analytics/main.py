from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

max_wait_time = 5

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    # driver.maximize_window()  # Maximize the Chrome window
    return driver

def get_business_info(driver, business_url):
    driver.get(business_url)
    
    business_info = {}
    
    try:
        # Get business name
        business_name_element = WebDriverWait(driver, max_wait_time).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@class="DUwDvf lfPIob"]'))
        )
        business_info['name'] = business_name_element.text

        # Get rating
        rating_element = WebDriverWait(driver, max_wait_time).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "F7nice ")]/span/span[@aria-hidden="true"]'))
        )
        business_info['rating'] = rating_element.text

        # Get reviews count
        reviews_count_element = WebDriverWait(driver, max_wait_time).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "F7nice ")]/span/span/span[@aria-label and not(@aria-hidden="true")]'))
        )
        business_info['reviews_count'] = reviews_count_element.text.strip("()")
        # For address
        try:
                address_element = WebDriverWait(driver, max_wait_time).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L "]//button[@aria-label][contains(@aria-label, "Address")]/div[@class="AeaXub"]/div[@class="rogA2c "]/div[@class="Io6YTe fontBodyMedium kR99db "]'))
                )
                business_info['full_address'] = address_element.text
        except TimeoutException:
                print("Full address not found")

        # For contact
        try:
                contact_element = WebDriverWait(driver, max_wait_time).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="RcCsl fVHpi w4vB1d NOE9ve M0S7ae AG25L "]//button[@aria-label][contains(@aria-label, "Phone")]/div[@class="AeaXub"]/div[@class="rogA2c "]/div[@class="Io6YTe fontBodyMedium kR99db "]'))
                )
                business_info['contact_number'] = contact_element.text
        except TimeoutException:
                print("Contact number not found")

                
        # Get website link
        try:
            website_element = WebDriverWait(driver, max_wait_time).until(
                EC.presence_of_element_located((By.XPATH, '//a[@data-item-id="authority"]'))
            )
            business_info['website'] = website_element.get_attribute("href")
        except TimeoutException:
            print("Website not found")

        return business_info
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main(business_url):
    driver = init_driver()
    
    try:
        # Get business information
        print("Retrieving business information...")
        business_info = get_business_info(driver, business_url)
        print('\n\t***********\t\n')
        if business_info:
            for key, value in business_info.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        else:
            print("Failed to retrieve business information.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the driver quits even if an error occurs
        driver.quit()


if __name__ == "__main__":
    # Replace this with the actual Google Maps URL of the business you want to analyze
    business_url = "https://www.google.com/maps/place/Sizzle/@31.4775527,74.3039139,16.62z/data=!4m14!1m7!3m6!1s0x391903f9ad1e9ff7:0xa24d3a595c3e6fef!2sMalwari+Paratha+Kabab!8m2!3d31.4785549!4d74.3089355!16s%2Fg%2F12mkzj3xj!3m5!1s0x3919030046a6ec49:0x11940be137db4968!8m2!3d31.4753041!4d74.306336!16s%2Fg%2F11v_0q1tbj?entry=ttu	"
    main(business_url)
