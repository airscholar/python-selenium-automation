from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()

service = webdriver.chrome.service.Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=service, options=options)

for i in range(1000):
    browser.get("https://voting-url.com")

    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Sample User')]")))
    element.click()

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Vote')]")))
    element.click()

    try:
        close_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "hustle-icon-close")))
        close_button.click()
    except:
        print("Popup not found or cannot be closed.")

    # Switch back to the original tab
    browser.switch_to.window(browser.window_handles[0])

    if i % 5 == 0:
        # get a list of all open tabs
        handles = browser.window_handles

        # iterate through the list of tabs (except the first one)
        for handle in handles[1:]:
            # switch to the tab
            browser.switch_to.window(handle)
            # close the tab
            browser.close()

        # switch back to the first tab
        browser.switch_to.window(browser.window_handles[0])

    browser.execute_script("window.scrollBy(0, 100);")
    # wait for 5 seconds
    time.sleep(2)

    poll_buttons = browser.find_elements(By.CSS_SELECTOR, "input.ays_finish_poll")
    if poll_buttons:
        poll_buttons[0].click()
    else:
        print("Could not find the poll button.")

    time.sleep(2)
    #refresh
    browser.refresh()


print("Done.")
time.sleep(5)
browser.quit()
