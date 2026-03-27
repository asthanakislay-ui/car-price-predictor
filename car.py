import streamlit as st
import pickle
import pandas as pd

# =========================
# LOAD MODEL + COLUMNS
# =========================
model = pickle.load(open('model.pkl', 'rb'))
columns = pickle.load(open('columns.pkl', 'rb'))

# =========================
# TITLE
# =========================
st.title(" Car Price Predictor")

# =========================
# INPUTS
# =========================
year = st.number_input("Year of Purchase", 2000, 2025)
km_driven = st.number_input("Kilometers Driven")

# fuel options (can adjust if needed)
fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])

# dynamically get company list from columns
company_list = [col.split("_")[1] for col in columns if col.startswith("company_")]
company = st.selectbox("Company", sorted(company_list))

# =========================
# PREDICTION
# =========================
if st.button("Predict Price"):
    
    # create input dictionary with all features = 0
    input_dict = {col: 0 for col in columns}

    # fill numeric values
    if 'year' in input_dict:
        input_dict['year'] = year

    if 'kms_driven' in input_dict:
        input_dict['kms_driven'] = km_driven

    # encode fuel
    fuel_col = f"fuel_{fuel}"
    if fuel_col in input_dict:
        input_dict[fuel_col] = 1

    # encode company
    company_col = f"company_{company}"
    if company_col in input_dict:
        input_dict[company_col] = 1

    # convert to dataframe
    input_df = pd.DataFrame([input_dict])

    # prediction
    prediction = model.predict(input_df)

    # output
    st.success(f"Estimated Price: ₹ {prediction[0]:,.2f}")