**Amazon Automation Web Scraping Project**
This project automates the web scraping process for fetching product details (such as mobiles and laptops) from Amazon India. It utilizes Selenium to extract information like product titles, ratings, prices, and MRP. The scraped data is saved into a CSV file for further analysis.

**Project Overview**
Purpose: To automate data extraction for electronic gadgets (e.g., mobiles, laptops) based on user-specified criteria.
**Key Features:**
Search for specific products on Amazon.
Filter by brand and customer ratings.
Extract details like product title, rating, current price, and MRP.
Save the extracted data into a results.csv file.
****Project Structure****
**amazon_scraper.py**

Contains the main Python script to perform web scraping using Selenium.
Core functionalities include:
Product search based on user input.
Brand and rating-based filtering.
Recursive navigation for pagination.
CSV export of scraped data.

**requirements.txt**

Contains the list of required Python packages and their versions.
**results.csv**

Sample result file containing scraped laptop data for demonstration.
Import Statements
The following Python packages are used in the project:

time: For introducing delays.
selenium: For browser automation and scraping.
pandas: For data manipulation and saving results into a CSV file.


**Limitations**
The script works specifically for Amazon India.
Dynamic changes in Amazon's website structure might require updates to the scraping logic.
Ensure compliance with Amazon's terms of service when using this script.
**Future Enhancements**
Add support for additional product categories.
Implement multi-threading for faster data extraction.
Add features for visualizing the scraped data using libraries like Matplotlib or Plotly.

**Disclaimer**
This project is for educational purposes only. Use the script responsibly and ensure adherence to Amazon's terms of service.

