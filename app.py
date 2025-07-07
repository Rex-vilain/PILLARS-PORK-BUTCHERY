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
import streamlit as st
import pandas as pd
import os
from datetime import datetime

 #Setup folder for saving/loading data 
DATA_DIR = "daily_data"
os.makedirs(DATA_DIR, exist_ok=True)

st.title("Pillars Pork Butchery Sales & Expenses")

 #Price inputs
st.sidebar.header("Set Prices per Kg / Item")
pork_takeaway_price = st.sidebar.number_input("Pork Takeaway (per kg)", min_value=1, value=650)
pork_ready_price = st.sidebar.number_input("Pork Ready (per kg)", min_value=1, value=800)
ugali_price = st.…
[12:14, 07/07/2025] Rex: "Payment Method": ["Cash"] * rows
}
df_sales = pd.DataFrame(data)

item_options = [""] + list(default_prices.keys())
payment_options = ["Cash", "Mpesa"]

column_config = {
    "Item": st.column_config.SelectboxColumn("Item", options=item_options),
    "Price per Kg": st.column_config.NumberColumn("Price per Kg", disabled=True),
    "Amount Paid": st.column_config.NumberColumn("Amount Paid", min_value=0.0),
    "Weight (Kg)": st.column_config.NumberColumn("Weight (Kg)", disabled=True),
    "Payment Method": st.column_config.SelectboxColumn("Payment Method", options=payment_options)
}

edited_sales = st.data_editor(df_sales, column_config=column_config, num_rows="fixed", key="sales_data")

 #Auto-calculate price and weight
for i, row in edited_sales.iterrows():
    item = row["Item"]
    price = default_prices.get(item, 0)
    edited_sales.at[i, "Price per Kg"] = price
    amount_paid = row["Amount Paid"]
    weight = round(amount_paid / price, 3) if price > 0 else 0
    edited_sales.at[i, "Weight (Kg)"] = weight

st.dataframe(edited_sales, use_container_width=True)

 # Daily Expenses
st.header("Daily Expenses")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

with st.form("expenses_form", clear_on_submit=True):
    col1, col2 = st.columns([3,1])
    desc = col1.text_input("Description")
    amt = col2.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")
    if submitted and desc and amt > 0:
        st.session_state.expenses.append({"Description": desc, "Amount": amt})

if st.session_state.expenses:
    df_expenses = pd.DataFrame(st.session_state.expenses)
    st.table(df_expenses)
else:
    df_expenses = pd.DataFrame(columns=["Description", "Amount"])
    st.write("No expenses added yet.")

 #Totals & Profit
total_sales_amount = edited_sales["Amount Paid"].sum()
total_expenses = df_expenses["Amount"].sum()
profit = total_sales_amount - total_expenses

st.markdown(f"Total Sales Amount: Ksh {total_sales_amount:.2f}")
st.markdown(f"Total Expenses: Ksh {total_expenses:.2f}")
st.markdown(f"## Profit: Ksh {profit:.2f}")

 # Save / Load Data 

st.header("Save or Load Data by Date")

def save_data(date_str):
    data = {
        "prices": default_prices,
        "sales": edited_sales.to_dict(orient="records"),
        "expenses": st.session_state.expenses
    }
    filename = os.path.join(DATA_DIR, f"{date_str}.json")
    pd.Series(data).to_json(filename)
    st.success(f"Data saved for {date_str}")

def load_data(date_str):
   filename = os.path.join(DATA_DIR, f"{date_str}.json")
    if os.path.exists(filename):
        data = pd.read_json(filename, typ='series')
        prices = data["prices"]
        sales = pd.DataFrame(data["sales"])
        expenses = pd.DataFrame(data["expenses"])
        return prices, sales, expenses
    else:
        st.error("No data found for that date.")
        return None, None, None

 #date_to_load = st.date_input("Select Date to Load", value=datetime.today())
if st.button("Load Data"):
    loaded_prices, loaded_sales, loaded_expenses = load_data(date_to_load.strftime("%Y-%m-%d"))
    if loaded_prices:
        st.write("### Loaded Prices")
        st.json(loaded_prices)
        st.write("### Loaded Sales")
        st.dataframe(loaded_sales)
        st.write("### Loaded Expenses")
        st.dataframe(loaded_expenses)

 #date_to_save = st.date_input("Select Date to Save Data", value=datetime.today(), key="save_date")
if st.button("Save Data"):
    save_data(date_to_save.strftime("%Y-%m-%d"))


#Expenses Table
st.header("Daily Expenses")

# Ensure expense columns exist in sales_data before accessing
if "Expense Description" not in sales_data.columns:
    sales_data["Expense Description"] = ""
if "Expense Amount" not in sales_data.columns:
    sales_data["Expense Amount"] = 0

exp_desc = []
exp_amt = []
max_exp_rows = 5

for i in range(max_exp_rows):
    cols_exp = st.columns(2)
    # Ensure sales_data has enough rows and the columns exist before accessing
    desc_val = sales_data["Expense Description"][i] if i < len(sales_data) and "Expense Description" in sales_data.columns and pd.notna(sales_data["Expense Description"][i]) else ""
    amt_val = sales_data["Expense Amount"][i] if i < len(sales_data) and "Expense Amount" in sales_data.columns and pd.notna(sales_data["Expense Amount"][i]) else 0
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
# Assuming price_pr for both Pork and Chicken Ready, and price_pt for Pork and Chicken Takeaway
df_sales["Pork Ready Weight (kg)"] = df_sales["Pork Ready"].apply(lambda x: calc_weight(price_pr, x))
df_sales["Pork Takeaway Weight (kg)"] = df_sales["Pork Takeaway"].apply(lambda x: calc_weight(price_pt, x))
df_sales["Chicken Ready Weight (kg)"] = df_sales["Chicken Ready"].apply(lambda x: calc_weight(price_pr, x))
df_sales["Chicken Takeaway Weight (kg)"] = df_sales["Chicken Takeaway"].apply(lambda x: calc_weight(price_pt, x))
#For chips and ugali weights just keep amounts as is (no kg)
df_sales["Chips Qty"] = df_sales["Chips"]
df_sales["Ugali Qty"] = df_sales["Ugali"]


# The sales_numeric_cols list should reflect the actual columns being summed
sales_numeric_cols = [
    "Pork Ready", "Pork Takeaway", "Chicken Ready", "Chicken Takeaway", "Chips", "Ugali"
]

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
    # Need to handle potential index mismatch if shapes are different
    # A simple concat might not be the best way if rows don't align
    # For now, let's save sales and expenses separately or ensure alignment
    # Assuming max_rows is used for both sales and expenses input
    # If not, adjust accordingly
    combined_df = pd.DataFrame()
    # Add sales data
    for col in manual_input_cols:
        combined_df[col] = data[col]
    # Add expense data
    combined_df["Expense Description"] = exp_desc
    combined_df["Expense Amount"] = exp_amt

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
        # This only displays the loaded data. Need to update the input widgets
        # to reflect the loaded data for editing. This is a more complex state
        # management issue in Streamlit. For now, just displaying is sufficient
        # based on the original code's behavior.
        st.dataframe(loaded)
