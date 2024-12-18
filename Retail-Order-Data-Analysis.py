import streamlit as st
import pandas as pd
import numpy as np
import psycopg2 

def get_db_connection():
    conn = psycopg2.connect (
    host = "mini-project.cfqqi6uos8nl.ap-south-1.rds.amazonaws.com",
    user = "postgres",
    password = "Password123",
    port = 5432,
    database = "postgres")

    return conn

def execute_query(query):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            return pd.DataFrame(data, columns=columns)
    finally:
        conn.close()

# Add color to the title
st.markdown("<h1 style='color: black;'>Retail Order Data Analysis</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color: black;'>SQL Queries</h2>", unsafe_allow_html=True)

# Add a colored sidebar
st.sidebar.markdown(
    """
    <style>
    .stSidebar {
        background-color: #818589; /* Gunmetal Gray */
    }
    </style>
    """,
    unsafe_allow_html=True
)
#query group selection 
query_group = st.sidebar.selectbox(
    "Category Selection:",
    ["Provided Queries", "Own Queries"]
)

query_options = {"Provided Queries":{
    "1. Top 10 Highest Revenue Generating Products":""" 
        select sd.sub_category, sd.product_id, sum(sd.sale_price) as total_revenue from sales_details sd join orders_details od 
        on sd.product_id = od.product_id group by sd.sub_category, sd.product_id order by total_revenue desc limit 10;""",
    "2. Top 5 Cities with the Highest Profit Margins": """
        select od.city, sum (case when sd.sale_price = 0 then 0 else (1-(sd.profit) / (sd.sale_price * sd.quantity)) * 100 end) as profit_margin from sales_details sd 
        join orders_details od on sd.order_id = od.order_id group by od.city order by profit_margin desc limit 5;""",
    "3. Total Discount Given for Each Category": """
        select category, sum(discount_amount) as total_discount from sales_details group by category order by total_discount desc;""",
    "4. Average Sale Price Per Product Category": """
        select category, avg(sale_price) as average_sale_price from sales_details group by category;""",
    "5. Region with the Highest Average Sale Price": """
        select region, avg(sale_price) as average_sale_price from sales_details join orders_details on 
        sales_details.order_id = orders_details.order_id group by region order by average_sale_price desc limit 1;""",
    "6. Total Profit Per Category": """
        select category, sum(profit) as total_profit from sales_details group by category order by total_profit desc;""",
    "7. Top 3 Segments with the Highest Quantity of Orders": """
        with quantity_data as (select segment, sum(quantity) as quantity_of_orders from sales_details join orders_details 
        on sales_details.order_id = orders_details.order_id group by segment) select segment, quantity_of_orders from quantity_data 
        order by quantity_of_orders desc limit 3;""",
    "8. Average Discount Percentage Per Region": """
        select region, (sum(discount_amount) / sum(sale_price)) * 100 as average_discount_percentage from sales_details join 
        orders_details on sales_details.order_id = orders_details.order_id group by region order by average_discount_percentage desc;""",
    "9. Product Category with the Highest Total Profit": """
        select category, sum(profit) as total_profit from sales_details group by category order by total_profit desc limit 1;""",
    "10. Total Revenue Generated Per Year": """
        select year, sum(sale_price) as total_revenue from sales_details group by year order by year;"""},
"Own Queries": {
    "1. Total sales amount by region":"""
        select region, sum(sale_price) as total_sales from orders_details join sales_details 
        on orders_details.order_id = sales_details.order_id group by region;""",
    "2. Top 5 best-selling products by quantity":"""
        select product_id, sum(quantity) as total_quantity from sales_details group by product_id
        order by total_quantity desc limit 5;""",
    "3. Average discount percentage by category":"""
        select category, avg(discount_percent) as avg_discount from sales_details group by category;""",
    "4. Monthly sales trend for a specific year":"""
        select month, sum(sale_price) as total_sales from sales_details where year = 2023
        group by month order by month;""",
    "5. Profitability by product":"""
        select product_id, sum(profit) as total_profit from sales_details group by product_id
        order by total_profit desc;""",
    "6. Number of orders per shipping mode":"""
        select ship_mode, count(distinct order_id) as order_count from orders_details group by ship_mode;""",
    "7. Total discount amount by state":"""
        select state, sum(discount_amount) as total_discount from orders_details join sales_details on 
        orders_details.order_id = sales_details.order_id group by state order by total_discount desc;""",
    "8. Regions with the highest profit margins":"""
        select region, sum(profit) / sum(cost_price) as profit_margin from orders_details join sales_details on 
        orders_details.order_id = sales_details.order_id group by region order by profit_margin desc;""",
    "9. Sales performance by segment":"""
        select segment, sum(sale_price) as total_sales from orders_details join sales_details on 
        orders_details.order_id = sales_details.order_id group by segment;""",
    "10.Identify underperforming products with negative profit":"""
        select product_id, sum(profit) as profit from sales_details group by product_id having sum(profit) < 0;"""}}

#select your queries

filter_queries = query_options.get(query_group,{})    
if not filter_queries:
    st.error(f"No queries found:{query_group}")
query_choice = st.selectbox("Select Query", list(filter_queries.keys()))

#Filter button
if st.button("Click Here!"):
    query = filter_queries.get(query_choice, " ")
    if query:
        try:
            data = execute_query(query)
            st.success("Result!")
            st.subheader("Answer")
            st.dataframe(data)
            if query_choice == "1. Top 10 Highest Revenue Generating Products":
                st.bar_chart(data.set_index("sub_category")["total_revenue"])
            elif query_choice == "2. Top 5 Cities with the Highest Profit Margins":
                st.bar_chart(data.set_index("city")["profit_margin"])
            elif query_choice == "3. Total Discount Given for Each Category":
                st.bar_chart(data.set_index("category")["total_discount"])
            elif query_choice == "4. Average Sale Price Per Product Category":
                st.bar_chart(data.set_index("category")["average_sale_price"])
            elif query_choice == "5. Region with the Highest Average Sale Price":
                st.write("Region with the Highest Average Sale Price : ", data.iloc[0]["region"])
            elif query_choice == "6. Total Profit Per Category":
                st.bar_chart(data.set_index("category")["total_profit"])
            elif query_choice == "7. Top 3 Segments with the Highest Quantity of Orders":
                st.bar_chart(data.set_index("segment")["quantity_of_orders"])
            elif query_choice == "8. Average Discount Percentage Per Region":
                st.bar_chart(data.set_index("region")["average_discount_percentage"])
            elif query_choice == "9. Product Category with the Highest Total Profit":
                st.bar_chart(data.set_index("category")["total_profit"])
            elif query_choice == "10. Total Revenue Generated Per Year":
                st.bar_chart(data.set_index("year")["total_revenue"])
        except Exception as e:
            st.error(f"Error executing query: {e}")
    else:
        st.error("No query selected.")