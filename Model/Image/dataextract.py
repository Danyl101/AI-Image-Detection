import time
import json
import os
import logging
import traceback
from httpx import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Logging function to capture log messsages 
logging.basicConfig(
    filename='Loader.log',
    level=logging.INFO,  # Change to DEBUG for more detail
    format='%(asctime)s - %(levelname)s - %(message)s'
)

output_dir="Dataset/AI_Images" #Establishes path of output directory for ai generated images
os.makedirs(output_dir,exist_ok=True)#Creates the output directory

def setup_driver(): #Setup Chrome WebDriver
    try:
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox") #Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")  # Add this if you're running headless
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) #Creates a web driver instance
        logging.info("Chrome WebDriver initialized successfully.") #Log message
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize Chrome WebDriver: {e}") #Log error message
        raise

def generate_ai_image():
    input_image_path=os.path.abspath(r"C:\Users\danyl\OneDrive\Desktop\Personal\Professional.jpg") #Defines a path for input image
    try:
        driver = setup_driver() #Initializes the driver 
        driver.get("https://gemini.google.com/app/8ada52bf684ca92e?hl=en-IN") #Driver grabs the link and runs on this link
        logging.info("Navigated to Gemini page.")
    except Exception as e:
        logging.error(f"Driver setup or navigation failed: {e}")
        return

    try:
        driver.find_elements(By.XPATH, '//p[contains(@class, "query-text-line")]') #Finds the DOM element of prompt ,done due to react loading elements after page loads
        
        driver.find_elements(By.XPATH, '//img[@data-test-id="uploaded-img"]') #Finds the DOM element of image upload ,done due to react loading elements after page loads
        
        img_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "image-button")]//img')) #Finds the DOM element of generaetd ,done due to react loading elements after page loads
        )  
        img_url = img_elem.get_attribute("src")
        
        logging.info("Uploaded image and submitted prompt.")
    except Exception as e:
        logging.error(f"Failed to upload or prompt: {e}")
        driver.quit()
        return

    try:
        time.sleep(15)  # Waiting for image to generate
        if not img_url: #Checks if img url is present
            raise Exception("Image URL is empty.")
        logging.info(f"Found generated image URL: {img_url}")
    except Exception as e:
        logging.error(f"Failed to locate generated image or extract URL: {e}")
        driver.quit() #Closes driver
        return

    try:
        response = requests.get(img_url, stream=True) #Requests img url from the driver 
        if response.status_code == 200: #Checks whether response is successful
            output_path = os.path.join(output_dir, os.path.basename(input_image_path)) #Sets the name of the image generated to be the same as that of the image uploaded
            with open(output_path, "wb") as f: #Writes into folder 
                for chunk in response.iter_content(1024): #I dont know explain
                    f.write(chunk) #I dont know explain
            logging.info(f"Image saved successfully at: {output_path}") #Log message
        else:
            logging.error(f"Image download failed with status code: {response.status_code}") #Log message
    except Exception as e:
        logging.error(f"Failed to download image: {e}")
    finally:
        driver.quit() # Driver closes
        logging.info("Browser closed.")
        
if __name__ == "__main__":
    generate_ai_image() #Function Called

    
    
