
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(layout="wide")
st.title("🐖 Pork Business Daily Stock Sheet")

#Constants for pricing
PRICES = {
    "Pork Takeaway": 650,
    "Pork Ready": 800,
    "Ugali": 50,
    "Chips": 100
}

#Input total sales
st.subheader("📊 Enter Total Sales")
sales_data = {}
quantities = {}

for item, price in PRICES.items():
    total = st.number_input(f"{item} Sales (Ksh)", min_value=0, step=50)
    qty = total / price if price > 0 else 0
    sales_data[item] = total
    quantities[item] = round(qty, 2)

#Display table
st.subheader("🧮 Auto-Calculated Quantities")
summary_df = pd.DataFrame({
    "Item": list(sales_data.keys()),
    "Total Sales (Ksh)": list(sales_data.values()),
    "Unit Price (Ksh)": list(PRICES.values()),
    "Quantity Sold": list(quantities.values())
})
st.dataframe(summary_df, use_container_width=True)

#Save file
today = datetime.now().strftime("%Y-%m-%d")
save_dir = "pork_data"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
summary_df.to_csv(f"{save_dir}/{today}_sales.csv", index=False)
