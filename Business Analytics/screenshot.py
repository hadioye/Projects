import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()  # Maximize the Chrome window
    return driver

def take_screenshot(driver, element, filename):
    element.screenshot(filename)

def create_screenshots_folder():
    folder_name = 'Screenshots'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def capture_reviews_screenshots(driver, url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load, adjust as necessary

    try:
        # Click the 'See all reviews' button to open the reviews dialog
        see_all_reviews_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "See all reviews")]'))
        )
        see_all_reviews_button.click()
        
        time.sleep(5)  # Wait for the reviews dialog to load
        
        # Scroll down to load more reviews
        scrollable_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="review-dialog-list"]'))
        )
        
        # Collect top reviews
        reviews = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="ODSEW-ShBeI NIyLF-haAclf gm2-body-2"]'))
        )
        
        folder_name = create_screenshots_folder()
        for index, review in enumerate(reviews[:5]):  # Taking top 5 reviews
            tagline = review.find_element(By.XPATH, './/span[@class="ODSEW-ShBeI-title"]').text[:10]  # Adjust as needed
            filename = os.path.join(folder_name, f'review_{index+1}_{tagline}.png')
            take_screenshot(driver, review, filename)
            print(f"Saved screenshot: {filename}")
    except Exception as e:
        print(f"Error capturing reviews: {e}")

def main():
    url = 'https://www.google.com/maps/place/Sizzle/@31.4775527,74.3039139,16.62z/data=!4m14!1m7!3m6!1s0x391903f9ad1e9ff7:0xa24d3a595c3e6fef!2sMalwari+Paratha+Kabab!8m2!3d31.4785549!4d74.3089355!16s%2Fg%2F12mkzj3xj!3m5!1s0x3919030046a6ec49:0x11940be137db4968!8m2!3d31.4753041!4d74.306336!16s%2Fg%2F11v_0q1tbj?entry=ttu'  # Replace with your Google Maps link
    driver = setup_driver()
    try:
        capture_reviews_screenshots(driver, url)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
