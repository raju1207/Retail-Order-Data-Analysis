import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="mini-project1.cp8i4gemw4g0.eu-north-1.rds.amazonaws.com",
        user="postgres",
        password="Miniproject1",
        port=5432,
        database="postgres"
    )

# Query execution
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

# Title
st.markdown("<h1 style='color: black;'>Retail Order Data Analysis</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='color: white;'>Query Selection</h2>", unsafe_allow_html=True)

# Sidebar background color
st.markdown(
    """<style>
    .stSidebar { background-color: #818589; }
    </style>""",
    unsafe_allow_html=True
)

# Queries
query_groups = {
    "Top Queries": {
        "1. Find top 10 highest revenue generating products": """select o.category,s.product_id,cast(sum(s.sale_price*s.quantity)as int) as total_revenue
    from sales_details as s join order_details as o on o.order_id=s.order_id
    group by o.category,s.product_id order by total_revenue desc limit 10;
    """,
            "2. Find the top 5 cities with the highest profit margins": """select o.city,sum(s.profit) as total_profit from sales_details as s
    join order_details as o on o.order_id=s.order_id group by o.city order by total_profit desc limit 5;
    """,
            "3. Calculate the total discount given for each category":"""select o.category,cast(sum(s.discount*s.quantity)as int)as total_discount from order_details as o
    join sales_details as s on s.order_id=o.order_id group by o.category ;
    """,
            "4. Find the average sale price per product category":"""select o.category,cast(avg(s.sale_price)as real) as avg_sale_price from order_details as o
    join sales_details as s on s.order_id=o.order_id group by o.category order by avg_sale_price desc;
    """,
            "5. Find the region with the highest average sale price":"""select o.region,cast(avg(s.sale_price)as real) as avg_sale_price from order_details as o
    join sales_details as s on s.order_id=o.order_id group by o.region order by region desc;
    """,
            "6. Find the total profit per category":"""select o.category,cast(sum(s.profit)as real) as total_profit from sales_details as s
    join order_details as o on o.order_id=s.order_id group by o.category;
    """,
            "7. Identify the top 3 segments with the highest quantity of orders":"""select o.category,o.segment,sum(s.quantity) as highest_quantity_orders from sales_details as s
    join order_details as o on o.order_id=s.order_id group by o.segment,o.category order by highest_quantity_orders desc limit 3;
    """,
            "8. Determine the average discount percentage given per region":"""select o.region,avg(s.discount_percent)as avg_discount_percentage from sales_details as s
    join order_details as o on o.order_id=s.order_id group by o.region;
    """,    
            "9. Find the product category with the highest total profit":"""select o.category ,s.profit from sales_details as s
    join order_details as o on o.order_id=s.order_id order by profit desc limit 1;
    """,    
            "10. Calculate the total revenue generated per year":"""select extract(year from o.order_date) as year,cast(sum(s.sale_price*s.quantity)as int) as total_revenue
    from sales_details as s join order_details as o on o.order_id=s.order_id group by year;
    """
    },

    "Custom Queries": {
            "1. Identify the top-selling product in each region":"""select o.region,o.category,cast(sum(s.quantity*s.sale_price)as int) as total_sales from sales_details as s
    join order_details as o on o.order_id=s.order_id group by region,category order by total_sales desc limit 10;
    """,
        "2. Calculate the total revenue generated per month":"""select extract(month from o.order_date) as month,cast(sum(s.sale_price*s.quantity)as int) as total_revenue
    from sales_details as s join order_details as o on o.order_id=s.order_id group by month order by month;
    """,
        "3. Find the Top-Selling Products by Category":"""select o.category,sum(s.quantity) as top_sales from sales_details as s
    join order_details as o on o.order_id=s.order_id group by o.category order by top_sales desc ;
    """,
        "4. Find the Yearly Profit Analysis":"""select extract(year from o.order_date)as year,cast(sum(s.profit)as int) as total_profit from sales_details as s
    join order_details as o on o.order_id=s.order_id group by year;
    """,
        "5. Calculate Order Count by Region":"""select o.region,sum(s.quantity) as order_count from sales_details as s
    join order_details as o on o.order_id=s.order_id group by o.region;
    """,
        "6. What Are Products with Discounts Above 3%":"""select o.category,s.discount_percent from sales_details as s
    join order_details as o on o.order_id=s.order_id  WHERE s.discount_percent > 3 AND s.discount_percent IS NOT NULL
    group by discount_percent,category order by discount_percent;
    """,
        "7. Find the Low-revenue Products below 1lack":"""select o.sub_category,cast(sum(s.sale_price * s.quantity)as int) as total_revenue from sales_details as s
    join order_details as o on o.order_id=s.order_id group by o.sub_category having sum(s.sale_price * s.quantity) < 100000 order by total_revenue asc
    """,
        "8. Find the top 10 order_id who generated the highest total revenue":"""select o.order_id,cast(sum(s.sale_price * s.quantity)as int) as total_revenue from sales_details as s
    join order_details as o on o.order_id=s.order_id group by o.order_id order by total_revenue desc limit 10;
    """,
        "9. Calculate the total amount of discount in all month":"""select extract(month from o.order_date)as month ,cast(sum(s.discount)as int)as discount_amount from sales_details as s
    join order_details as o on o.order_id=s.order_id group by month order by month;
    """,
        "10. Calculate the average discount percentage for each region":"""select o.region, round(avg(s.discount_percent),2) as avg_discount_percent from sales_details as s
    join order_details as o on o.order_id=s.order_id group by region;
    """ 
    }
}

group = st.sidebar.selectbox("Choose Query Group", list(query_groups.keys()))
query_dict = query_groups[group]
query_label = st.sidebar.selectbox("Select a Query", list(query_dict.keys()))
query_sql = query_dict[query_label]

# Chart type selection
chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar", "Line", "Area", "Scatter", "Pie"])

# Execute and display
if st.button("Run Query"):
    try:
        df = execute_query(query_sql)
        st.success("Query executed successfully!")
        st.write("### Data Preview", df)

        # Try to identify the two best columns to plot
        if len(df.columns) >= 2:
            x_col, y_col = df.columns[:2]
        else:
            st.warning("Not enough columns to plot.")
            x_col = y_col = None

        if x_col and y_col:
            if chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col, title=query_label)
            elif chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col, title=query_label)
            elif chart_type == "Area":
                fig = px.area(df, x=x_col, y=y_col, title=query_label)
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_col, y=y_col, title=query_label)
            elif chart_type == "Pie":
                fig = px.pie(df, names=x_col, values=y_col, title=query_label)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Chart not rendered due to missing data.")

    except Exception as e:
        st.error(f"Error: {e}")
