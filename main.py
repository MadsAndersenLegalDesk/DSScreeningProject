import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def fetch_data(db_file, query):
    """Fetches data from the SQLite database using the provided query."""
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.title("Simple E-commerce Dashboard")
    db_file = 'legal_documents_ecommerce.db'

    # --- Overall Metrics ---
    st.subheader("Overall Metrics")
    col1, col2, col3, col4 = st.columns(4)

    # Total Customers
    customers_df = fetch_data(db_file, "SELECT COUNT(*) FROM Customers")
    total_customers = customers_df.iloc[0, 0]
    col1.metric("Total Customers", total_customers)

    # Total Products
    products_df = fetch_data(db_file, "SELECT COUNT(*) FROM Products")
    total_products = products_df.iloc[0, 0]
    col2.metric("Total Products", total_products)

    # Total Orders
    orders_df = fetch_data(db_file, "SELECT COUNT(*) FROM Orders")
    total_orders = orders_df.iloc[0, 0]
    col3.metric("Total Orders", total_orders)

    # Total Revenue
    revenue_df = fetch_data(db_file, "SELECT SUM(total_amount) FROM Orders")
    total_revenue = revenue_df.iloc[0, 0] if revenue_df.iloc[0, 0] else 0
    col4.metric("Total Revenue", f"${total_revenue:.2f}")

    # --- Orders Over Time ---
    st.subheader("Orders Over Time")
    orders_over_time_df = fetch_data(db_file, """
        SELECT strftime('%Y-%m', order_date) AS order_month, COUNT(*) AS num_orders
        FROM Orders
        GROUP BY order_month
        ORDER BY order_month
    """)
    if not orders_over_time_df.empty:
        fig_orders_over_time = px.line(orders_over_time_df, x='order_month', y='num_orders',
                                     title='Number of Orders per Month')
        st.plotly_chart(fig_orders_over_time)
    else:
        st.info("No order data available for the orders over time chart.")

    # --- Product Category Distribution ---
    st.subheader("Product Category Distribution")
    category_distribution_df = fetch_data(db_file, """
        SELECT category, COUNT(*) AS num_products
        FROM Products
        GROUP BY category
    """)
    if not category_distribution_df.empty:
        fig_category_distribution = px.pie(category_distribution_df, values='num_products', names='category',
                                          title='Distribution of Products by Category')
        st.plotly_chart(fig_category_distribution)
    else:
        st.info("No product data available for the category distribution chart.")

if __name__ == "__main__":
    main()
