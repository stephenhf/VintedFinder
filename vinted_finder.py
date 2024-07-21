
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define your search parameters
keywords = os.getenv("KEYWORDS").split(",")
max_price = os.getenv("MAX_PRICE")
email_address = os.getenv("EMAIL_ADDRESS")
app_password = os.getenv("APP_PASSWORD")
recipient_email = os.getenv("RECIPIENT_EMAIL")

# Set up Selenium WebDriver
options = Options()
options.headless = True  # Run in headless mode (without opening a browser window)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to fetch listings from Vinted
def fetch_listings(keyword):
    url = f"https://www.vinted.co.uk/catalog?search_text={keyword}&price_to={max_price}"
    driver.get(url)
    
    # Wait for the listings to be present
    try:
        listings_present = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.feed-grid__item'))
        WebDriverWait(driver, 10).until(listings_present)
    except Exception as e:
        print(f"Error waiting for listings: {e}")
        return []
    
    # Debugging: print out a snippet of the page source to verify structure
    print(f"Fetching listings for keyword: {keyword}")
    print("HTML Snippet:
", driver.page_source[:1000])  # Print the first 1000 characters of the HTML

    return driver.find_elements(By.CSS_SELECTOR, '.feed-grid__item')

# Function to extract listing details
def extract_listing_details(listing):
    try:
        price = listing.find_element(By.CSS_SELECTOR, 'p.web_ui__Text__text.web_ui__Text__subtitle.web_ui__Text__left.web_ui__Text__clickable.web_ui__Text__underline-none').text.strip()
    except:
        price = "No price found"
    try:
        link_element = listing.find_element(By.CSS_SELECTOR, 'a.new-item-box__overlay.new-item-box__overlay--clickable')
        link = link_element.get_attribute('href')
        title = link_element.get_attribute('title').split(',')[0]  # Extract title from the 'title' attribute
    except:
        link = "No link found"
        title = "No title found"
    try:
        # Precise CSS selector for the listing image
        image = listing.find_element(By.CSS_SELECTOR, 'div.new-item-box__image img').get_attribute('src')
    except:
        image = "No image found"
    
    # Debug prints
    print(f"Extracted details - Title: {title}, Price: {price}, Link: {link}, Image: {image}")
    
    return title, price, link, image

# Function to send email with HTML formatting including images
def send_email(listings):
    subject = "Vinted Listings By VintedFinder"
    body = "<html><body>"
    
    for keyword, items in listings.items():
        body += f"<h2>Listings for keyword '{keyword}':</h2><ul>"
        for title, price, link, image in items:
            body += f"<li><b>Title:</b> {title}<br><b>Price:</b> {price}<br><b>Link:</b> <a href='{link}'>{link}</a><br><img src='{image}' alt='{title}' style='width:150px;height:auto;'></li><br>"
        body += "</ul><br>"  # Add an extra newline for separation between keywords
    
    body += "</body></html>"  # Close the HTML tags
    
    # Debug print for email body
    print("Email Body:
", body)

    msg = MIMEMultipart("alternative")
    msg['From'] = email_address
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, app_password)
    text = msg.as_string()
    server.sendmail(email_address, recipient_email, text)
    server.quit()

# Main function
def main():
    listings = {}

    for keyword in keywords:
        fetched_listings = fetch_listings(keyword)
        if not fetched_listings:
            print(f"No listings found for keyword: {keyword}")
        extracted_listings = [extract_listing_details(listing) for listing in fetched_listings]
        listings[keyword] = extracted_listings

        # Debug print
        print(f"Keyword: {keyword}")
        for listing in extracted_listings:
            print(listing)

    if listings:
        send_email(listings)
    else:
        print("No listings to send in email.")

if __name__ == "__main__":
    main()
    driver.quit()  # Ensure the browser is closed
