from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Create a new instance of Chrome WebDriver
driver = webdriver.Chrome()

# Function to extract product details from the product page
def extract_product_details(url):
    # Open the product URL
    driver.get(url)
    
    # Wait for the product page to load (title, price, and description should be available)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-title")))

    # Extract title
    try:
        title = driver.find_element(By.CLASS_NAME, "product-title").text
    except:
        title = "Not Available"
    
    # Extract price
    try:
        price = driver.find_element(By.CSS_SELECTOR, "div.measurements-selector__product-price span").text
    except:
        price = "Not Available"
    
    # Extract description
    try:
        description = driver.find_element(By.ID, "fc_index_0").find_element(By.TAG_NAME, "p").text
    except:
        description = "Not Available"
    
    return title, price, description

# Open the CSV file containing product links and read the links
with open('product_links.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    product_links = [row[0] for row in reader]

# Create a new CSV file to save the product details
with open('product_details.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Description", "Link"])  # Write header

    # Loop through each product link
    for link in product_links:
        try:
            # Extract product details
            title, price, description = extract_product_details(link)
            
            # Write product details to CSV
            writer.writerow([title, price, description, link])
            
            # Optional: Delay between requests to avoid overwhelming the server
            time.sleep(2)
        except Exception as e:
            print(f"Failed to extract details for {link}: {e}")
            continue

# Close the browser
driver.quit()

print("Product details extraction complete.")
