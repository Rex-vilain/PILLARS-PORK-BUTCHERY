
import streamlit as st
import pandas as pd
import os
from datetime import datetime

#Setup 
st.set_page_config(layout="wide")
st.title("🐖 Pork Business Daily Tracker")

#Editable Prices
st.sidebar.header("Set Prices per Kg / Item")
pork_takeaway_price = st.sidebar.number_input("Pork Takeaway (per kg)", value=650)
pork_ready_price = st.sidebar.number_input("Pork Ready (per kg)", value=800)
ugali_price = st.sidebar.number_input("Ugali", value=50)
chips_price = st.sidebar.number_input("Chips", value=100)

#Date Handling 
today = st.date_input("Select Date", value=datetime.today()).strftime("%Y-%m-%d")
folder = "pork_logs"
if not os.path.exists(folder):
    os.makedirs(folder)

filename = f"{folder}/{today}.csv"
expenses_filename = f"{folder}/{today}_expenses.csv"


#Sales Entry 
st.subheader("🍖 Sales Entry")
cols = ["Pork Takeaway", "Payment PT", "Pork Ready", "Payment PR", "Ugali", "Payment Ugali", "Chips", "Payment Chips"]
default_data = pd.DataFrame(columns=cols)

if os.path.exists(filename):
    sales_data = pd.read_csv(filename)
else:
    sales_data = default_data

edited_sales = st.data_editor(
    sales_data,
    use_container_width=True,
    num_rows="dynamic",
    key="sales"
)

#Calculate Totals 
def calc_weight(col, price):
    return col / price if price else 0


edited_sales["Pork Takeaway"] = pd.to_numeric(edited_sales["Pork Takeaway"], errors="coerce").fillna(0)
edited_sales["Pork Ready"] = pd.to_numeric(edited_sales["Pork Ready"], errors="coerce").fillna(0)

edited_sales["PT Weight (kg)"] = edited_sales["Pork Takeaway"] / pork_takeaway_price if pork_takeaway_price else 0
edited_sales["PR Weight (kg)"] = edited_sales["Pork Ready"] / pork_ready_price if pork_ready_price else 0

#Convert columns to numeric safely, replace NaNs with 0, then sum
total_pt = pd.to_numeric(edited_sales["Pork Takeaway"], errors="coerce").fillna(0).sum()
total_pr = pd.to_numeric(edited_sales["Pork Ready"], errors="coerce").fillna(0).sum()
total_ugali = pd.to_numeric(edited_sales["Ugali"], errors="coerce").fillna(0).sum()
total_chips = pd.to_numeric(edited_sales["Chips"], errors="coerce").fillna(0).sum()

#Expenses Entry 
st.subheader("🧾 Daily Expenses")
if os.path.exists(expenses_filename):
    expenses_df = pd.read_csv(expenses_filename)
else:
    expenses_df = pd.DataFrame(columns=["Description", "Amount"])

edited_expenses = st.data_editor(
    expenses_df,
    use_container_width=True,
    num_rows="dynamic",
       key="expenses"
)

total_expenses = edited_expenses["Amount"].sum() if not edited_expenses.empty else 0
profit = total_sales - total_expenses

#Summary 
st.subheader("📊 Daily Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"Ksh {total_sales:,.0f}")
col2.metric("Total Expenses", f"Ksh {total_expenses:,.0f}")
col3.metric("Net Profit", f"Ksh {profit:,.0f}")

#Save Button 
if st.button("💾 Save Today's Data"):
    edited_sales.to_csv(filename, index=False)
    edited_expenses.to_csv(expenses_filename, index=False)
    st.success("Data saved successfully!")

# View Past Records 
st.subheader("📁 View Past Records")
log_files = sorted([f for f in os.listdir(folder) if f.endswith(".csv") and "expenses" not in f])

selected_file = st.selectbox("Select a date to view:", log_files)
if selected_file:
    past_sales = pd.read_csv(f"{folder}/{selected_file}")
    st.write("Sales Data:")
    st.dataframe(past_sales, use_container_width=True)

    exp_file = selected_file.replace(".csv", "_expenses.csv")
    if os.path.exists(f"{folder}/{exp_file}"):
        past_exp = pd.read_csv(f"{folder}/{exp_file}")
        st.write("Expenses Data:")
        st.dataframe(past_exp, use_container_width=True)
    else:
        st.warning("No expense data for that day.")
