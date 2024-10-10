import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu
from prediction_helper import predict

# Set the page configuration and title
st.set_page_config(page_title="Fintree Finance: Credit Risk Modelling", page_icon="📊", layout="wide")

#

# Page header
st.markdown(
    "<h1 style='text-align: center; color: #4B8BBE;'>Fintree Finance: Credit Risk Modelling</h1>",
    unsafe_allow_html=True
)

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Manual Input", "Upload Data"],
        icons=["pencil-square", "cloud-upload"],
        menu_icon="app-indicator",
        default_index=0,
        styles={
            "container": {"padding": "5px"},
            "icon": {"color": "#4B8BBE"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "10px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#4B8BBE"},
        },
    )

# Function to process ratings
def process_rating(rating):
    ratings_map = {
        "Excellent": "Excellent",
        "Good": "Good",
        "Average": "Average",
        "Poor": "Poor"
    }
    return ratings_map.get(rating, rating)

# Function to process the uploaded file
def process_uploaded_file(file):
    # Read the uploaded Excel file
    data = pd.read_excel(file)

    # Initialize empty lists to store results
    probabilities = []
    credit_scores = []
    ratings = []

    # Iterate over each row and calculate the results
    for _, row in data.iterrows():
        # Extract values for each column needed by the predict function
        age = row['age']
        income = row['income']
        loan_amount = row['loan_amount']
        loan_tenure_months = row['loan_tenure_months']
        avg_dpd_per_delinquency = row['avg_dpd_per_delinquency']
        delinquency_ratio = row['delinquency_ratio']
        credit_utilization_ratio = row['credit_utilization_ratio']
        num_open_accounts = row['number_of_open_accounts']
        residence_type = 'Owned' if row['residence_type_Owned'] else 'Rented' if row['residence_type_Rented'] else 'Mortgage'
        loan_purpose = 'Education' if row['loan_purpose_Education'] else 'Home' if row['loan_purpose_Home'] else 'Auto' if row['loan_purpose_Auto'] else 'Personal'
        loan_type = 'Unsecured' if row['loan_type_Unsecured'] else 'Secured'

        # Calculate prediction results
        probability, credit_score, rating = predict(
            age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type
        )

        # Append results to respective lists
        probabilities.append(probability)
        credit_scores.append(credit_score)
        ratings.append(process_rating(rating))

    # Add results to the DataFrame
    data['Default Probability'] = probabilities
    data['Credit Score'] = credit_scores
    data['Rating'] = ratings

    return data

# Handling the menu selections
if selected == "Manual Input":
    st.markdown("## Manual Input")

    # Create rows of three columns each for manual input
    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(3)
    row4 = st.columns(3)

    # Assign inputs to the first row with default values
    with row1[0]:
        age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28, help="Enter the applicant's age.")
    with row1[1]:
        income = st.number_input('Income', min_value=0, value=1200000, help="Enter the applicant's annual income.")
    with row1[2]:
        loan_amount = st.number_input('Loan Amount', min_value=0, value=2560000, help="Enter the loan amount requested.")

    # Calculate Loan to Income Ratio and display it
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    with row2[0]:
        st.text("Loan to Income Ratio:")
        st.text(f"{loan_to_income_ratio:.2f}")

    # Assign inputs to the remaining controls
    with row2[1]:
        loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36, help="Enter the loan tenure in months.")
    with row2[2]:
        avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=20, help="Average Days Past Due per delinquency.")

    with row3[0]:
        delinquency_ratio = st.number_input('Delinquency Ratio', min_value=0, max_value=100, step=1, value=30, help="Ratio of delinquent accounts to total accounts.")
    with row3[1]:
        credit_utilization_ratio = st.number_input('Credit Utilization Ratio', min_value=0, max_value=100, step=1, value=30, help="Percentage of available credit used.")
    with row3[2]:
        num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, step=1, value=2, help="Number of open loan accounts.")

    with row4[0]:
        residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'], help="Type of residence.")
    with row4[1]:
        loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'], help="Purpose of the loan.")
    with row4[2]:
        loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'], help="Type of loan.")

    # Button to calculate risk with hover effect
    if st.button('Calculate Risk', key='calculate-risk', help="Click to calculate the credit risk"):
        probability, credit_score, rating = predict(
            age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type
        )

        # Display the results
        st.markdown("### Prediction Results")
        st.write(f"**Default Probability:** {probability:.2%}")
        st.write(f"**Credit Score:** {credit_score}")
        st.write(f"**Rating:** {process_rating(rating)}")

elif selected == "Upload Data":
    st.markdown("## Upload Data")

    # Sub-tabs within Upload Data
    upload_tab, analysis_tab = st.tabs(["Data Upload", "Data Analysis"])

    # Upload Excel file
    with upload_tab:
        uploaded_file = st.file_uploader("Upload an Excel file", type=['xlsx'], help="Upload an Excel file with the required columns.")
        
        
    if uploaded_file is not None:
        # Process uploaded file and display results
        df = process_uploaded_file(uploaded_file)
        st.markdown("### Credit Risk Analysis Results")
        st.dataframe(df.style.format({"Default Probability": "{:.2%}", "Credit Score": "{:.0f}"}))
        

        # Activate the Data Analysis sub-tab
        with analysis_tab:
            if uploaded_file is None:
              st.markdown("<div class='warning'>Please upload an Excel file to proceed with data analysis.</div>", unsafe_allow_html=True)

            st.markdown("### Visualize Data")

            # Select parameters for the x and y axes
            x_param = st.selectbox('Select X-axis parameter:', options=df.columns)
            y_param = st.selectbox('Select Y-axis parameter:', options=df.columns)

            # Select chart type
            chart_type = st.selectbox('Select chart type:', ['Bar Chart', 'Pie Chart', 'Histogram'])

            # Button to generate the chart with hover effect
            if st.button('Generate Chart', key='generate-chart', help="Click to generate a chart based on selected parameters"):
                if chart_type == 'Bar Chart':
                    st.markdown(f"### Bar Chart: {x_param} vs {y_param}")
                    fig = px.bar(df, x=x_param, y=y_param)
                    st.plotly_chart(fig)

                elif chart_type == 'Pie Chart':
                    st.markdown(f"### Pie Chart: Distribution of {x_param}")
                    fig = px.pie(df, names=x_param)
                    st.plotly_chart(fig)

                elif chart_type == 'Histogram':
                    st.markdown(f"### Histogram: {x_param}")
                    fig = px.histogram(df, x=x_param, nbins=20)
                    st.plotly_chart(fig)

# Footer
st.markdown('<hr style="border:1px solid gray">', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;">_Fintree Finance Credit Risk Modelling App_</div>', unsafe_allow_html=True)
