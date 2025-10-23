import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv("startup_funding.csv")
print(df.shape)

# Clean column names
df.columns = df.columns.str.strip().str.replace(' +', '_', regex=True)

# Drop unnecessary columns
df.drop(columns=['Sr_No', 'Remarks', 'SubVertical'], inplace=True)

# Convert Amount_in_USD to numeric
df['Amount_in_USD'] = df['Amount_in_USD'].replace('[\$,]', '', regex=True)
df['Amount_in_USD'] = pd.to_numeric(df['Amount_in_USD'], errors='coerce')

# Fill missing values
df['Amount_in_USD'].fillna(df['Amount_in_USD'].mean(), inplace=True)
df['City_Location'].fillna('Lucknow', inplace=True)
df['Industry_Vertical'].fillna('IT', inplace=True)

print(df.isnull().sum())

# Convert date and extract year
df['Date_dd/mm/yyyy'] = pd.to_datetime(df['Date_dd/mm/yyyy'], format='%d/%m/%Y', errors='coerce')
df['Date_dd/mm/yyyy'] = df['Date_dd/mm/yyyy'].dt.year
print(df.head(3))

# ---------------- DASHBOARD ----------------
st.title("DASHBOARD FOR INDIAN STARTUP FUNDING")

# Sidebar filters
year = st.sidebar.selectbox("Choose Year", ['2019', '2020'])
year = int(year)

company = st.sidebar.selectbox('Choose Company', df['Startup_Name'])
total_funding = df['Amount_in_USD'].sum()
st.metric("💰 Total Funding", f"${total_funding:,.0f}")
total_startups = df['Startup_Name'].nunique()
st.metric("🏢 Total Startups Funded", total_startups)
avg_funding = df['Amount_in_USD'].mean()
st.metric("📈 Average Funding per Startup", f"${avg_funding:,.0f}")
total_investors = df['Investors_Name'].nunique()
st.metric("👥 Total Investors", total_investors)
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Funding", f"${total_funding:,.0f}")
col2.metric("🏢 Total Startups", total_startups)
col3.metric("📈 Average Funding per Startup", f"${avg_funding:,.0f}")

# Total funding for selected year
df_year = df[df['Date_dd/mm/yyyy'] == year]
funding = df_year['Amount_in_USD'].sum()
st.write(f"The total funding in the year {year} is ${funding:,.0f}")

# Funding for selected company
df_company = df[df['Startup_Name'] == company]
company_funding = df_company['Amount_in_USD'].sum()
st.success(f"The funding to {company} is ${company_funding:,.0f}")

# Top cities
cityfunding = df.groupby('City_Location')['Amount_in_USD'].sum()
cityfunding = cityfunding.sort_values(ascending=False)
topcities = cityfunding.head(5)

# Pie chart for top funding cities
plt.figure(figsize=(4,4))
topcities.plot.pie(autopct='%1.1f%%', title='Top 5 Cities by Funding')
plt.ylabel('')
st.pyplot(plt)

# Top companies
topcompanies = df.groupby('Startup_Name')['Amount_in_USD'].sum()
topcompanies = topcompanies.sort_values(ascending=False)
topcompanieslist = topcompanies.head(5)

# Bar graph for top companies
plt.figure(figsize=(4,4))
topcompanieslist.plot.bar(title="TOP COMPANIES")
plt.ylabel("Amount in USD")
st.pyplot(plt)





