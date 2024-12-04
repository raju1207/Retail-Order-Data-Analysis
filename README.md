# Orders Dataset Analysis
This repository contains a dataset and accompanying analysis for understanding order trends in a retail business.

## Dataset Overview
The dataset includes information about 9,994 orders, detailing customer demographics, product categories, and sales metrics. Below are the main columns and their descriptions:

## Columns
- **Order Id:** Unique identifier for each order.
- **Order Date:** Date when the order was placed.
- **Ship Mode:** Mode of shipment for the order (e.g., Second Class, Standard Class).
- **Segment:** Customer segment (e.g., Consumer, Corporate).
- **Country:** Country where the order was placed (all entries are "United States").
- **City:** City of the customer.
- **State:** State of the customer.
- **Postal Code:** Postal code of the customer.
- **Region:** Region of the customer (e.g., South, West).
- **Category:** Product category (e.g., Furniture, Office Supplies).
- **Sub Category:** Product subcategory (e.g., Bookcases, Labels).
- **Product Id:** Unique identifier for each product.
- **Cost Price:** Cost of the product for the retailer.
- **List Price:** Retail price of the product.
- **Quantity:** Number of units ordered.
- **Discount Percent:** Discount applied to the order (in percentage).

## Dataset Summary
- **Number of Rows:** 9,994
- **Number of Columns:** 16
- **Missing Data:** Minimal, with only one missing value in the "Ship Mode" column.

## Sample Data
|``Order Id``	| ``Order Date``	| ``Ship Mode``	| ``Segment``	| ``Country``	| ``City``	| ``...`` |
|-------------|----------------|---------------|-------------|-------------|----------|---------|
|1	 |2023-03-01	|Second Class|	Consumer	|United States|	Henderson|	...|
|2	 |2023-08-15	|Second Class|	Consumer	|United States|	Henderson|	...|
|3	 |2023-01-10	|Second Class|	Corporate|United States|	Los Angeles|	...|

## Repository Contents
- ``orders.csv``: The dataset file.
- ``analysis.ipynb``: A Jupyter notebook for exploring and analyzing the data.
- ``README.md``: This documentation file.

## Potential Analysis Goals
 1. **Sales Trends:** Understand patterns in sales over time.
 2. **Regional Performance:** Compare sales and profitability across different regions.
 3. **Product Insights:** Identify top-performing product categories and subcategories.
 4. **Discount Effectiveness:** Analyze the impact of discounts on sales.

## Usage Instructions
 1. Clone the repository:
   > ```git clone https://github.com/yourusername/orders-dataset-analysis.git```
   > 
 2. Install necessary Python libraries:
   > ```pip install pandas matplotlib seaborn```
   >  
 3. Open the analysis notebook for detailed exploration:
   > ```jupyter notebook analysis.ipynb```
   > 

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.
