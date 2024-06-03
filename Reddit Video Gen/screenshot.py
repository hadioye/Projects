from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
# Config
screenshotDir = "Screenshots"
screenWidth = 400
screenHeight = 800

def getPostScreenshots(filePrefix, script):
    print("Taking screenshots...")
    driver, wait = __setupDriver(script.url)
    script.titleSCFile = __takeScreenshot(filePrefix, driver, wait, "Post")
    for commentFrame in script.frames:
        commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, f"t1_{commentFrame.commentId}")
    driver.quit()


def __takeScreenshot(filePrefix, driver, wait, handle="Post"):
    try:
        time.sleep(2)
        if handle == "Post":
            # Find the element containing the post title based on its ID attribute
            search = wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(@id,'post-title-')]")))
        else:
            # Find the element containing the comment based on its ID attribute
            search = wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(@id,'{handle}-comment-rtjson-content')]")))
        
        driver.execute_script("window.focus();")

        # Ensure the screenshot directory exists
        os.makedirs(screenshotDir, exist_ok=True)
        fileName = os.path.join(screenshotDir, f"{filePrefix}-{handle}.png")

        # Save the screenshot using a context manager
        with open(fileName, "wb") as fp:
            fp.write(search.screenshot_as_png)

        return fileName
    except TimeoutException:
        print(f"Element '{handle}' not found within the given time.")
        return None


def __setupDriver(url: str):
    options = webdriver.FirefoxOptions()
    options.headless = False
    options.enable_mobile = False
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    driver.set_window_size(width=screenWidth, height=screenHeight)
    driver.get(url)

    return driver, wait
