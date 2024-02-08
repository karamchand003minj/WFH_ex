from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_data(url):
    # Set up Chrome WebDriver
    service = Service(executable_path="chromedriver.exe")
    # driver = webdriver.Chrome(service=service)
    # service = Service('/path/to/chromedriver')  # Replace '/path/to/chromedriver' with the path to your chromedriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Optional: Run headless
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Navigate to the URL
    driver.get(url)
    
    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "div")))
    
    # Extract data from div tags
    div_data = [div.text for div in driver.find_elements(By.TAG_NAME, "div")]
    
    # Quit the WebDriver
    driver.quit()
    
    return div_data

# Example usage
if __name__ == "__main__":
    url = "https://www.the-afc.com/en/livescores/afc_competitions/afc_cup.html"  # Replace with your desired URL
    div_data = extract_data(url)
    
    if div_data:
        print("Data from <div> tags:")
        for data in div_data:
            print("-", data)
