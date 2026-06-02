from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import pymongo
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import time


# MongoDB Configuration
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["autodoc-data"]
mycol = mydb["new_links"]
data_collection = mydb['new_data']


# Function to create a browser instance using SeleniumBase
def create_browser():
    driver = Driver(
        browser="chrome",
        uc=True,  # Use undetected-chromedriver
        headless=True,  # Browser runs visibly but minimized
        incognito=True,
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36 AVG/112.0.21002.139",
        do_not_track=True,
        undetectable=True  # Enable stealth mode to bypass detection
    )
    # Minimize the browser window (move off-screen)
    driver.set_window_position(-2000, 0)
    return driver



# Initialize a pool of browser instances
browser_pool = [create_browser() for _ in range(1)]
browser_queue = Queue()


# Add browsers to the queue
for browser in browser_pool:
    browser_queue.put(browser)


# Function to process URLs
def processing(urls):
    url = urls['urls']
    driver = browser_queue.get()

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(3)

        # Locate and iterate over main elements
        main_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '(//div[@class="product-info-block__accordion"])[1]//div[@class="product-info-block__item"]'))
        )

        for element in main_elements:
            link = WebDriverWait(element, 10).until(
                EC.presence_of_element_located((By.XPATH, './a | ./span'))
            )
            driver.execute_script("arguments[0].click();", link)
            time.sleep(0.5)

            sub_elements = WebDriverWait(element, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, './ul/li'))
            )

            for sub_element in sub_elements:
                sub_link = WebDriverWait(sub_element, 10).until(
                    EC.presence_of_element_located((By.XPATH, './span'))
                )
                driver.execute_script("arguments[0].click();", sub_link)
                time.sleep(0.5)

        # Parse the page content using lxml
        time.sleep(1)
        page_content = html.fromstring(driver.page_source)
        all_rows = page_content.xpath('//div[@class="product-info-block__accordion"]/div')

        # Extract and save data
        for row in all_rows:
            temp_data = {'URL': url}
            fitment1 = row.xpath('./span/text() | ./a/text()')
            temp_data['Fitment-1'] = ' '.join(fitment1).strip()
            sub_rows = row.xpath('./ul/li')

            for sub_row in sub_rows:
                fitment2 = sub_row.xpath('./span/text()')
                sub_temp_data = temp_data.copy()
                sub_temp_data['Fitment-2'] = ' '.join(fitment2).strip()
                third_rows = sub_row.xpath('./ul/li')

                for third_row in third_rows:
                    fitment3 = third_row.xpath('./text()')
                    third_temp_data = sub_temp_data.copy()
                    third_temp_data['Fitment-3'] = ' '.join(fitment3).strip()
                    data_collection.insert_one(third_temp_data)
                    print(third_temp_data)

        # Mark the URL as processed in MongoDB
        mycol.update_one({"_id": urls['_id']}, {"$set": {"status": "DONE"}})

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

    finally:
        # Return the browser to the queue
        browser_queue.put(driver)

# Main Execution
if __name__ == '__main__':
    # Get all pending links
    all_links = list(mycol.find({'status': 'PENDING'}))

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(processing, link) for link in all_links]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing a link: {e}")

    # Clean up browser instances
    while not browser_queue.empty():
        driver = browser_queue.get()
        driver.quit()
