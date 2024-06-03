from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_business_info(driver, business_url):
    driver.get(business_url)
    
    try:
        # Get business name
        business_name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@class="DUwDvf lfPIob"]'))
        )
        business_name = business_name_element.text

        # Get rating
        rating_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "F7nice ")]/span/span[@aria-hidden="true"]'))
        )
        rating = rating_element.text

        # Get full address
        address_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-item-id="address"]//div[@class="Io6YTe fontBodyMedium kR99db"]'))
        )
        full_address = address_element.text

        # Get opening hours
        opening_hours_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Hours"]//span[@class="ZDu9vd"]'))
        )
        opening_hours = opening_hours_element.text

        # Get contact number
        contact_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-item-id="phone:tel:042111656565"]//div[@class="Io6YTe fontBodyMedium kR99db"]'))
        )
        contact_number = contact_element.text

        # Get website link
        website_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-item-id="authority"]'))
        )
        website = website_element.get_attribute("href")

        return {
            "name": business_name,
            "rating": rating,
            "full_address": full_address,
            "opening_hours": opening_hours,
            "contact_number": contact_number,
            "website": website
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
