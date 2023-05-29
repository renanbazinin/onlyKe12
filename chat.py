import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def random_sleep():
    sleep_time = random.randint(180, 300)  # Random time between 3 and 5 minutes in seconds
    time.sleep(sleep_time)
    
# Set up Chrome options to run headless (without opening a browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")

# Path to your ChromeDriver executable
chromedriver_path = '/path/to/chromedriver'

while True:
    # Set up the ChromeDriver service
    service = Service(chromedriver_path)

    # Launch Chrome browser
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Website URL to visit
    url = 'https://www.mako.co.il/mako-vod-live-tv/VOD-6540b8dcb64fd31006.htm'

    # Open the website
    driver.get(url)

    # Wait for the page to load completely
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Get the network requests captured by the browser
    network_entries = driver.execute_script("return window.performance.getEntriesByType('resource');")

    # Find the first network request that matches the URL prefix
    target_url = 'https://mako-streaming.akamaized.net/stream/hls/live/2033791/k12dvr/index.m3u8?b-in-range=100-2700'
    filtered_request = next((entry['name'] for entry in network_entries if entry['name'].startswith(target_url)), None)

    if filtered_request:
        # Create the text file and write the content
        with open('ke12.m3u', 'w') as file:
            file.write('#EXTM3U\n')
            file.write('#EXTINF:-1 tvg-id="Keshet 12 IL" tvg-name="Keshet 12 IL" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Keshet12_2018.svg/1200px-Keshet12_2018.svg.png" group-title="Israel",keshet12\n')
            file.write(filtered_request)
    else:
        print("No matching network request found.")

    # Close the browser
    driver.quit()

    # Delay for 3 minutes before the next execution
    random_sleep()
