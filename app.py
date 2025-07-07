import streamlit as st
import pandas as pd
import os
from datetime import datetime

#Folder to save data files
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

st.title("Pillars Pork & Chicken Restaurant Management")

#Price Settings 
st.sidebar.header("Set Prices per Kg / Item")
price_pt = st.sidebar.number_input("Pork Takeaway (per kg)", min_value=0, value=650, step=10)
price_pr = st.sidebar.number_input("Pork Ready (per kg)", min_value=0, value=800, step=10)
price_ug = st.sidebar.number_input("Ugali (per item)", min_value=0, value=50, step=5)
price_chips = st.sidebar.number_input("Chips (per item)", min_value=0, value=100, step=10)

#Input Date 
date_str = st.text_input("Enter Date to Load or Save Data (YYYY-MM-DD)", value=datetime.today().strftime("%Y-%m-%d"))

def data_filepath(date):
    return os.path.join(DATA_DIR, f"{date}.csv")

def load_data(date):
    path = data_filepath(date)
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        # Return empty DataFrame with correct columns
        cols = [
            "Pork Ready", "Pork Ready Pay",
            "Pork Takeaway", "Pork Takeaway Pay", 
            "Chicken Ready", "Chicken Ready Pay", 
            "Chicken Takeaway", "Chicken Takeaway Pay", 
            "Chips", "Chips Pay", 
            "Ugali", "Ugali Pay",
            "Expense Description", "Expense Amount"
        ]
        return pd.DataFrame(columns=cols)

#Sales Input Table
st.header("Sales Entry Table")

cols = [
    "Pork Ready", "Pork Ready Pay", 
    "Pork Takeaway", "Pork Takeaway Pay", 
    "Chicken Ready", "Chicken Ready Pay", 
    "Chicken Takeaway", "Chicken Takeaway Pay", 
    "Chips", "Chips Pay", 
    "Ugali", "Ugali Pay"
]

#Initial empty data or loaded data
sales_data = load_data(date_str)

#Sales columns numeric
sales_numeric_cols = [
    "Pork Ready", "Pork Takeaway", "Chicken Ready", "Chicken Takeaway", "Chips", "Ugali"
]

#Payment methods allowed
payment_methods = ["cash", "mpesa", ""]

#We’ll build an editable table row by row in streamlit with inputs
#Limit max rows (e.g. 10 rows)
max_rows = 10

data = {}
for col in cols:
    data[col] = []

st.write("Fill sales quantities and select payment method:")

for i in range(max_rows):
    cols 1 = st.columns(12)
    for j, col_name in enumerate(cols):
        if "Pay" in col_name:
                             data[col_name].append(cols1[j].selectbox(f"{col_name} (Row {i+1})", payment_methods, index=2, key=f"{col_name}_{i}"))
        else:
            val = sales_data[col_name][i] if i < len(sales_data) and pd.notna(sales_data[col_name][i]) else 0
            data[col_name].append(cols1[j].number_input(f"{col_name} (Row {i+1})", min_value=0, value=int(val), key=f"{col_name}_{i}"))

df_sales = pd.DataFrame(data)

#Expenses Table
st.header("Daily Expenses")

if "Expense Description" not in sales_data.columns:
    sales_data["Expense Description"] = ""
if "Expense Amount" not in sales_data.columns:
    sales_data["Expense Amount"] = 0

exp_desc = []
exp_amt = []
max_exp_rows = 5

for i in range(max_exp_rows):
    cols_exp = st.columns(2)
    desc_val = sales_data["Expense Description"][i] if i < len(sales_data) and pd.notna(sales_data["Expense Description"][i]) else ""
    amt_val = sales_data["Expense Amount"][i] if i < len(sales_data) and pd.notna(sales_data["Expense Amount"][i]) else 0
    exp_desc.append(cols_exp[0].text_input(f"Description {i+1}", value=desc_val, key=f"desc_{i}"))
    exp_amt.append(cols_exp[1].number_input(f"Amount {i+1}", min_value=0, value=int(amt_val), key=f"amt_{i}"))

df_expenses = pd.DataFrame({
    "Expense Description": exp_desc,
    "Expense Amount": exp_amt
})

#Calculations 

def calc_weight(price, amount):
    return amount / price if price > 0 else 0

#Calculate weights
df_sales["Pork Ready Weight (kg)"] = df_sales["Pork Ready"].apply(lambda x: calc_weight(price_pr, x))
df_sales["Pork Takeaway Weight (kg)"] = df_sales["Pork Takeaway"].apply(lambda x: calc_weight(price_pt, x))
df_sales["Chicken Ready Weight (kg)"] = df_sales["Chicken Ready"].apply(lambda x: calc_weight(price_pr, x))  # assuming same price as pork ready?
df_sales["Chicken Takeaway Weight (kg)"] = df_sales["Chicken Takeaway"].apply(lambda x: calc_weight(price_pt, x))  # assuming same price as pork takeaway?
For chips and ugali weights just keep amounts as is (no kg)
df_sales["Chips Qty"] = df_sales["Chips"]
df_sales["Ugali Qty"] = df_sales["Ugali"]

total_sales = df_sales[sales_numeric_cols].sum().sum()
total_expenses = df_expenses["Expense Amount"].sum()
profit = total_sales - total_expenses

st.write(f"Total Sales: KES {total_sales:.2f}")
st.write(f"Total Expenses: KES {total_expenses:.2f}")
st.write(f"Profit: KES {profit:.2f}")

#Save / Load Buttons
st.header("Save / Load Daily Data")

if st.button("Save Current Data"):
    # Combine sales and expenses into one DataFrame for saving
    combined_df = pd.concat([df_sales, df_expenses], axis=1)
    combined_df.to_csv(data_filepath(date_str), index=False)
    st.success(f"Data saved for date {date_str}")

#Load Data Section
st.subheader("Load Data for Date")
date_to_load = st.text_input("Enter date to load (YYYY-MM-DD)", value=date_str, key="load_date")
if st.button("Load Data"):
    loaded = load_data(date_to_load)
    if loaded.empty:
        st.info(f"No saved data found for {date_to_load}")
    else:
        st.dataframe(loaded)

