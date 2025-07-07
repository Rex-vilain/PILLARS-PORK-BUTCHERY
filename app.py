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
ugali_price = st.sidebar.number_input("Ugali (per item)", min_value=1, value=50)
chips_price = st.sidebar.number_input("Chips (per item)", min_value=1, value=100)
chicken_ready_price = st.sidebar.number_input("Chicken Ready (per kg)", min_value=1, value=750) # Example price
chicken_takeaway_price = st.sidebar.number_input("Chicken Takeaway (per kg)", min_value=1, value=600) # Example price


 #Data structure for sales
st.header("Daily Sales")

 #Ensure sales_data is in session state
if 'sales_data' not in st.session_state:
     #Load data if available for today, otherwise start empty
    today_str = datetime.today().strftime("%Y-%m-%d")
    filepath = os.path.join(DATA_DIR, f"{today_str}.csv")
    if os.path.exists(filepath):
        st.session_state.sales_data = pd.read_csv(filepath)
    else:
         #Initial empty dataframe with columns for sales and expenses
        cols = [
            "Pork Ready", "Pork Ready Pay",
            "Pork Takeaway", "Pork Takeaway Pay",
            "Chicken Ready", "Chicken Ready Pay",
            "Chicken Takeaway", "Chicken Takeaway Pay",
            "Chips", "Chips Pay",
            "Ugali", "Ugali Pay",
            "Expense Description", "Expense Amount"
        ]
        st.session_state.sales_data = pd.DataFrame(columns=cols)


 #Define default prices dictionary
default_prices = {
    "Pork Takeaway": pork_takeaway_price,
    "Pork Ready": pork_ready_price,
    "Ugali": ugali_price,
    "Chips": chips_price,
    "Chicken Ready": chicken_ready_price,
    "Chicken Takeaway": chicken_takeaway_price
}

 #We’ll build an editable table row by row in streamlit with inputs
 #Limit max rows (e.g. 10 rows)
max_rows = 10

data = {}
manual_input_cols = [
    "Pork Ready", "Pork Ready Pay",
    "Pork Takeaway", "Pork Takeaway Pay",
    "Chicken Ready", "Chicken Ready Pay",
    "Chicken Takeaway", "Chicken Takeaway Pay",
    "Chips", "Chips Pay",
    "Ugali", "Ugali Pay"
]
for col in manual_input_cols:
    data[col] = []

st.write("Fill sales quantities and select payment method:")

 #This part seems redundant with st.data_editor below. Let's remove or refactor.
 #Keeping it commented for now based on original code structure.
 #for i in range(max_rows):
 #    cols1 = st.columns(12)
 #    for j, col_name in enumerate(manual_input_cols):
 #        if "Pay" in col_name:
 #             # Ensure sales_data has enough rows before accessing it
 #             current_value = st.session_state.sales_data[col_name][i] if i < len(st.session_state.sales_data) and col_name in st.session_state.sales_data.columns and pd.notna(st.session_state.sales_data[col_name][i]) else ""
 #             # Find the index of the current value in payment_methods, default to 2 (empty string)
 #             selected_index = payment_methods.index(current_value) if current_value in payment_methods else 2
 #             data[col_name].append(cols1[j].selectbox(f"{col_name} (Row {i+1})", payment_methods, index=selected_index, key=f"{col_name}_{i}"))
 #        else:
 #            # Ensure sales_data has enough rows and the column exists before accessing it
 #            val = st.session_state.sales_data[col_name][i] if i < len(st.session_state.sales_data) and col_name in st.session_state.sales_data.columns and pd.notna(st.session_state.sales_data[col_name][i]) else 0
 #            data[col_name].append(cols1[j].number_input(f"{col_name} (Row {i+1})", min_value=0, value=int(val), key=f"{col_name}_{i}"))

#Use st.data_editor for sales input
st.subheader("Enter Sales Data")

#Prepare initial data for data_editor
#It seems there's a mix of row-based input and data_editor. Let's try to standardize with data_editor for sales.
#Creating a simple structure for data_editor based on typical sales entries.
#This will likely replace the manual_input_cols approach for sales.
rows = 10 # Number of initial rows for the data editor
initial_sales_editor_data = {
    "Item": [""] * rows,
    "Price per Kg": [0.0] * rows,
    "Amount Paid": [0.0] * rows,
    "Weight (Kg)": [0.0] * rows,
    "Payment Method": ["Cash"] * rows
}
df_sales_editor = pd.DataFrame(initial_sales_editor_data)

item_options = [""] + list(default_prices.keys())
payment_options = ["Cash", "Mpesa"]

column_config = {
    "Item": st.column_config.SelectboxColumn("Item", options=item_options),
    "Price per Kg": st.column_config.NumberColumn("Price per Kg", disabled=True, format="%.2f"),
    "Amount Paid": st.column_config.NumberColumn("Amount Paid", min_value=0.0, format="%.2f"),
    "Weight (Kg)": st.column_config.NumberColumn("Weight (Kg)", disabled=True, format="%.3f"),
    "Payment Method": st.column_config.SelectboxColumn("Payment Method", options=payment_options)
}

edited_sales = st.data_editor(df_sales_editor, column_config=column_config, num_rows="fixed", key="sales_data_editor")

#Auto-calculate price and weight
for i, row in edited_sales.iterrows():
    item = row["Item"]
    # Ensure the item exists in default_prices before accessing
    if item in default_prices:
        price = default_prices[item]
        edited_sales.at[i, "Price per Kg"] = price
        amount_paid = row["Amount Paid"]
        weight = round(amount_paid / price, 3) if price > 0 else 0
        edited_sales.at[i, "Weight (Kg)"] = weight
    else:
         # If item is not selected or not in prices, set price and weight to 0
        edited_sales.at[i, "Price per Kg"] = 0
        edited_sales.at[i, "Weight (Kg)"] = 0


st.dataframe(edited_sales, use_container_width=True)

#Daily Expenses
st.markdown("### Daily Expenses")

 #Editable table for expense entry
expenses_df = st.data_editor(
    pd.DataFrame(columns=["Expense Description", "Expense Amount"]),
    num_rows="dynamic",
    key="expenses"
)

 #Ensure numeric data for calculations
expenses_df["Expense Amount"] = pd.to_numeric(expenses_df["Expense Amount"], errors="coerce").fillna(0)

 #Calculate total expenses
total_expenses = expenses_df["Expense Amount"].sum()

 #Display total expenses and profit (make sure total_sales is defined above this block)
st.markdown(f"*Total Sales Amount:* Ksh {total_sales:,.2f}")
st.markdown(f"*Total Expenses:* Ksh {total_expenses:,.2f}")

 #Calculate and show profit
profit = total_sales - total_expenses
st.markdown(f"### *Profit: Ksh {profit:,.2f}*")


#Totals & Profit
total_sales_amount = edited_sales["Amount Paid"].sum()
total_expenses = st.session_state.expenses_df["Amount"].sum() if "Amount" in st.session_state.expenses_df.columns else 0 # Ensure column exists

st.markdown(f"Total Sales Amount: Ksh {total_sales_amount:.2f}")
st.markdown(f"Total Expenses: Ksh {total_expenses:.2f}")
profit = total_sales_amount - total_expenses
st.markdown(f"## Profit: Ksh {profit:.2f}")

# Save / Load Data

st.header("Save or Load Data by Date")

#Adjust save_data to save sales and expenses separately or in a structured format like JSON
def save_data(date_str, sales_df, expenses_df):
    data = {
        "sales": sales_df.to_dict(orient="records"),
        "expenses": expenses_df.to_dict(orient="records"),
        #Save prices as well
        "prices": default_prices # Or use st.session_state.prices if they are editable elsewhere
    }
    filename = os.path.join(DATA_DIR, f"{date_str}.json") # Save as JSON
    pd.Series(data).to_json(filename)
    st.success(f"Data saved for {date_str}")

#Adjust load_data to load from JSON and populate session state
def load_data_into_session_state(date_str):
    filename = os.path.join(DATA_DIR, f"{date_str}.json")
    if os.path.exists(filename):
        try:
            data = pd.read_json(filename, typ='series')
            #Load sales
            if "sales" in data:
                st.session_state.sales_df = pd.DataFrame(data["sales"])
            else:
                st.session_state.sales_df = pd.DataFrame(columns=["Item", "Price per Kg", "Amount Paid", "Weight (Kg)", "Payment Method"])

            #Load expenses
            if "expenses" in data:
                st.session_state.expenses_df = pd.DataFrame(data["expenses"])
            else:
                st.session_state.expenses_df = pd.DataFrame(columns=["Description", "Amount"])

            #Load prices
            if "prices" in data:
                st.session_state.prices = data["prices"]
            else:
                #If prices not saved, revert to default prices
                st.session_state.prices = default_prices.copy()

            st.success(f"Data loaded for {date_str}")
            st.rerun() # Rerun to update the UI with loaded data

        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.info("Loading failed, tables reset.")
            #Reset to empty dataframes on load error
            st.session_state.sales_df = pd.DataFrame(columns=["Item", "Price per Kg", "Amount Paid", "Weight (Kg)", "Payment Method"])
            st.session_state.expenses_df = pd.DataFrame(columns=["Description", "Amount"])

    else:
        st.error("No data found for that date.")
        #Optionally reset tables if no data is found
        #st.session_state.sales_df = pd.DataFrame(columns=["Item", "Price per Kg", "Amount Paid", "Weight (Kg)", "Payment Method"])
        #st.session_state.expenses_df = pd.DataFrame(columns=["Description", "Amount"])


#Date input for loading
date_to_load = st.text_input("Enter date to load (YYYY-MM-DD)", value=datetime.today().strftime("%Y-%m-%d"), key="load_date_input")

if st.button("Load Data"):
    load_data_into_session_state(date_to_load)

if st.button("Save Data"):
    #Save current state of data editors and prices
    save_data(date_str, edited_sales, edited_expenses)


#Expenses Table
#This section appears to be a duplicate or alternative approach to the st.data_editor for expenses.
#Let's remove it to avoid confusion and potential conflicts.
#st.header("Daily Expenses")

# Ensure expense columns exist in sales_data before accessing
#if "Expense Description" not in sales_data.columns:
#    sales_data["Expense Description"] = ""
#if "Expense Amount" not in sales_data.columns:
#    sales_data["Expense Amount"] = 0

#exp_desc = []
#exp_amt = []
#max_exp_rows = 5

#for i in range(max_exp_rows):
#    cols_exp = st.columns(2)
#    # Ensure sales_data has enough rows and the columns exist before accessing
#    desc_val = sales_data["Expense Description"][i] if i < len(sales_data) and "Expense Description" in sales_data.columns and pd.notna(sales_data["Expense Description"][i]) else ""
#    amt_val = sales_data["Expense Amount"][i] if i < len(sales_data) and "Expense Amount" in sales_data.columns and pd.notna(sales_data["Expense Amount"][i]) else 0
#    exp_desc.append(cols_exp[0].text_input(f"Description {i+1}", value=desc_val, key=f"desc_{i}"))
#    exp_amt.append(cols_exp[1].number_input(f"Amount {i+1}", min_value=0, value=int(amt_val), key=f"amt_{i}"))

#df_expenses = pd.DataFrame({
#    "Expense Description": exp_desc,
#    "Expense Amount": exp_amt
#})

#Calculations

#This section is calculating based on df_sales which is populated by the manual input loops above,
#but sales are now managed by edited_sales (from data_editor).
#Let's update the calculations to use the data from edited_sales and edited_expenses (from data_editor).

#def calc_weight(price, amount):
#    return amount / price if price > 0 else 0

#Calculate weights - this is now handled within the data_editor logic after editing
#Assuming price_pr for both Pork and Chicken Ready, and price_pt for Pork and Chicken Takeaway
#df_sales["Pork Ready Weight (kg)"] = df_sales["Pork Ready"].apply(lambda x: calc_weight(price_pr, x))
#df_sales["Pork Takeaway Weight (kg)"] = df_sales["Pork Takeaway"].apply(lambda x: calc_weight(price_pt, x))
#df_sales["Chicken Ready Weight (kg)"] = df_sales["Chicken Ready"].apply(lambda x: calc_weight(price_pr, x))
#df_sales["Chicken Takeaway Weight (kg)"] = df_sales["Chicken Takeaway"].apply(lambda x: calc_weight(price_pt, x))
#For chips and ugali weights just keep amounts as is (no kg)
#df_sales["Chips Qty"] = df_sales["Chips"]
#df_sales["Ugali Qty"] = df_sales["Ugali"]


# The sales_numeric_cols list should reflect the actual columns being summed
#This is now just the "Amount Paid" column from edited_sales
#sales_numeric_cols = [
#    "Pork Ready", "Pork Takeaway", "Chicken Ready", "Chicken Takeaway", "Chips", "Ugali"
#]

#total_sales = df_sales[sales_numeric_cols].sum().sum()
#total_expenses = df_expenses["Expense Amount"].sum()
#profit = total_sales - total_expenses

#st.write(f"Total Sales: KES {total_sales:.2f}")
#st.write(f"Total Expenses: KES {total_expenses:.2f}")
#st.write(f"Profit: KES {profit:.2f}")

#Save / Load Buttons
#This section is a duplicate of the save/load buttons above. Let's remove this one.
#st.header("Save / Load Daily Data")

#if st.button("Save Current Data"):
#    # Combine sales and expenses into one DataFrame for saving
#    # Need to handle potential index mismatch if shapes are different
#    # A simple concat might not be the best way if rows don't align
#    # For now, let's save sales and expenses separately or ensure alignment
#    # Assuming max_rows is used for both sales and expenses input
#    # If not, adjust accordingly
#    combined_df = pd.DataFrame()
#    # Add sales data
#    for col in manual_input_cols:
#        combined_df[col] = data[col]
#    # Add expense data
#    combined_df["Expense Description"] = exp_desc
#    combined_df["Expense Amount"] = exp_amt

#    combined_df.to_csv(data_filepath(date_str), index=False)
#    st.success(f"Data saved for date {date_str}")

#Load Data Section
#This section is a duplicate of the load section above. Let's remove this one.
#st.subheader("Load Data for Date")
#date_to_load = st.text_input("Enter date to load (YYYY-MM-DD)", value=date_str, key="load_date")
#if st.button("Load Data"):
#    loaded = load_data(date_to_load)
#    if loaded.empty:
#        st.info(f"No saved data found for {date_to_load}")
#    else:
#        # This only displays the loaded data. Need to update the input widgets
#        # to reflect the loaded data for editing. This is a more complex state
#        # management issue in Streamlit. For now, just displaying is sufficient
#        # based on the original code's behavior.
#        st.dataframe(loaded)
