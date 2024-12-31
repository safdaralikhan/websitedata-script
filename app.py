from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Function to extract product links from the main page
def get_product_links():
    # Open the main URL
    driver.get("https://plasticsheetsshop.co.uk/acrylic-sheets/")
    
    # Accept cookies
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonAccept"))).click()
    
    # Wait for the "Clear" category to be visible
    clear_category_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='teaser-product-category__title' and text()='Clear']/ancestor::a"))
    )
    
    # Scroll to the "Clear" category and click it
    ActionChains(driver).move_to_element(clear_category_link).perform()
    clear_category_link.click()
    
    # Wait for the product links to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "teaser-product__link")))
    
    # Extract product links
    product_elements = driver.find_elements(By.XPATH, "//li[@class='col-6 col-sm-6 col-md-4 has-button-favorite']//a[@class='teaser-product__link']")
    return [product.get_attribute("href") for product in product_elements]

# Function to extract product details from a product page
def extract_product_details(url):
    # Open the product page
    driver.get(url)
    
    # Wait for product details to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-title")))
    
    # Extract product details
    try:
        title = driver.find_element(By.CLASS_NAME, "product-title").text
    except:
        title = "Not Available"
    
    try:
        price = driver.find_element(By.CSS_SELECTOR, "div.measurements-selector__product-price span").text
    except:
        price = "Not Available"
    
    try:
        description = driver.find_element(By.ID, "fc_index_0").find_element(By.TAG_NAME, "p").text
    except:
        description = "Not Available"
    
    return title, price, description

# Main script logic
def main():
    # Step 1: Get all product links
    print("Extracting product links...")
    product_links = get_product_links()
    print(f"Found {len(product_links)} product links.")
    
    # Step 2: Extract details for each product link and save them to a CSV file
    with open('product_details.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Description", "Link"])  # Write header
        
        for link in product_links:
            try:
                print(f"Processing: {link}")
                title, price, description = extract_product_details(link)
                writer.writerow([title, price, description, link])
                time.sleep(2)  # Optional delay
            except Exception as e:
                print(f"Failed to process {link}: {e}")
    
    print("Product details extraction complete.")

# Run the main script
try:
    main()
finally:
    # Close the browser
    driver.quit()
