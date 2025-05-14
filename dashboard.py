import pandas as pd
import plotly.express as px
import streamlit as st

# Load and preprocess data
df = pd.read_csv("expense_data_1.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Month Name'] = df['Date'].dt.strftime('%b')

# App UI
st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")

with st.sidebar:
    st.title("Income Expense analysis")
    st.markdown("Overview of income and expense based on your bank transactions. Categories are obtained using local LLMs.")
    st.image("https://ouch-cdn2.icons8.com/vY_cFhHVmK7rcG3SKw0AAkHlAZp1MzHddsvzXDrrFrU/rs:fit:368:275/czM6Ly9pY29uczgvZXNzZW50aWFscy9wZW9wbGUtbWFuYWdlbWVudC1ncmFwaC1yZXBvcnQucG5n.png", width=250)

# Year tab selector
year = st.selectbox("Select Year", df['Year'].sort_values().unique())

# Filter by year
df_year = df[df['Year'] == year]

# Split into income and expense
income_df = df_year[df_year['Income/Expense'] == 'Income']
expense_df = df_year[df_year['Income/Expense'] == 'Expense']

# Calculations
total_income = income_df['Amount'].sum()
total_expense = expense_df['Amount'].sum()
saving_rate = round((total_income - total_expense) / total_income * 100, 2) if total_income > 0 else 0

# Layout: Top two donut charts
col1, col2 = st.columns(2)

with col1:
    income_by_cat = income_df.groupby('Category')['Amount'].sum().reset_index()
    fig_income = px.pie(income_by_cat, values='Amount', names='Category', hole=0.4,
                        title=f"Income Breakdown {year}", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_income.update_traces(textinfo='percent+label+value')
    st.plotly_chart(fig_income, use_container_width=True)

with col2:
    expense_by_cat = expense_df.groupby('Category')['Amount'].sum().reset_index()
    fig_expense = px.pie(expense_by_cat, values='Amount', names='Category', hole=0.4,
                         title=f"Expense Breakdown {year}: Saving rate {saving_rate}%",
                         color_discrete_sequence=px.colors.qualitative.Set3)
    fig_expense.update_traces(textinfo='percent+label+value')
    st.plotly_chart(fig_expense, use_container_width=True)

# Layout: Monthly income and expense bar charts
col3, col4 = st.columns(2)

with col3:
    income_monthly = income_df.groupby('Month Name')['Amount'].sum().reindex(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']).reset_index()
    fig_bar_income = px.bar(income_monthly, x='Month Name', y='Amount', text='Amount',
                            color='Amount', color_continuous_scale='Greens',
                            title="Income per month")
    st.plotly_chart(fig_bar_income, use_container_width=True)

with col4:
    expense_monthly = expense_df.groupby('Month Name')['Amount'].sum().reindex(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']).reset_index()
    fig_bar_expense = px.bar(expense_monthly, x='Month Name', y='Amount', text='Amount',
                             color='Amount', color_continuous_scale='OrRd',
                             title="Expense per month")
    st.plotly_chart(fig_bar_expense, use_container_width=True)
