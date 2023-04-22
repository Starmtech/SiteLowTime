import logging
import smtplib
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(filename='example.log', level=logging.INFO)

smtp_server = "smtp.example.com"
smtp_port = 587
smtp_username = "user@example.com"
smtp_password = "password"
from_address = "user@example.com"
to_address = "recipient@example.com"

class PageLoader:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.timeout = 10
    
    def load_page(self):
        try:
            self.driver.get(self.url)
        except TimeoutException:
            logging.error("Timeout occurred while loading the page")
            self.driver.quit()
            return None
        
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except TimeoutException:
            logging.error("Timeout occurred while waiting for page elements to load")
            self.driver.quit()
            return None
        
        try:
            page_load_time = self.driver.execute_script("return (window.performance.timing.loadEventEnd - window.performance.timing.navigationStart) / 1000")
        except Exception as e:
            logging.error(f"Error occurred while measuring page load time: {str(e)}")
            self.driver.quit()
            return None
        
        self.driver.quit()
        return page_load_time

while True:
    loader = PageLoader("https://www.example.com")
    page_load_time = loader.load_page()
    if page_load_time is None:
        logging.error("Failed to measure page load time")
        continue

    subject = "Page Load Time"
    message = f"The page loaded in {page_load_time:.2f} seconds"
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        msg = f"Subject: {subject}\n\n{message}"
        smtp.sendmail(from_address, to_address, msg)
        smtp.quit()
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")


    logging.info(f"Page load time: {page_load_time:.2f}")
    logging.info("Email sent with page load time")

    time.sleep(300)  # 5 minutes
