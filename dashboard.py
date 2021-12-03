from pathlib import WindowsPath
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit.util import index_


# Basic Page Configurations
st.set_page_config(page_title="VideoGame Sales Data",
                   page_icon=":bar_chart:",
                   layout="wide")
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style> """, unsafe_allow_html=True)


# adding dark theme to the plt plots
plt.style.use("dark_background")

# Adding Header
st.header("VideoGames Sales Data Visualization")


width = st.sidebar.slider("Width", min_value=6, max_value=20, value=10)
height = st.sidebar.slider("Height", min_value=1, max_value=10, value=3)


# loading data
data = pd.read_csv("./vgsales.csv")
data = data.dropna()  # dropping null values


# 1 Some Basic information about data
c0, c1, c2, c3 = st.columns(4)
c0.metric("Total Videogames", len(data))
c1.metric("Total Genre", len(data['Genre'].unique()))
c2.metric("Total Publishers", len(data['Publisher'].unique()))
c3.metric("Total Platforms", len(data['Platform'].unique()))

# 2 Checkbox to show dataset
if st.checkbox("Show Data"):
    st.write(data)


# 3 Total data data distribution according to Platform or Genre accornding to the selection
op = st.selectbox("Select one of the following", ["Platform", "Genre"])
st.subheader(op + " wise data distribution")
st.bar_chart(data[op].value_counts(), height=400, use_container_width=True)


# 4  Videogames Sales Data by years
# plt.figure(1)
fig, ax = plt.subplots(figsize=(width, height))
st.subheader("Salesdata by Year")
op1 = st.multiselect(
    "Select Sales Category", ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"], default=["Global_Sales"])
group1 = data.groupby('Year').sum()
ax.plot(group1[op1], label=op1)
ax.set_xlabel("Years")
ax.set_ylabel("Sales in Million")
ax.legend()
st.pyplot(fig)


# 5 PieCharts of various SalesData record
left, right = st.columns(2)
# 5.1 PieChart of Salesdata by region
left.subheader("SalesData by Region")
lst = []
plt.figure(2)
for i in data.columns[6:-1]:
    lst.append(sum(data[i]))

mlabels = data.columns[6:-1]
plt.pie(lst, labels=mlabels, autopct='%1.1f%%')
plt.legend()
plt.tight_layout()
left.pyplot(plt.figure(2))

# 5.2 Piechart of Salesdata by Genre
right.subheader("Salesdata by Genre")
plt.figure(3)
group1 = data.groupby('Genre').sum()
mlabels = data["Genre"].unique()
plt.pie(group1["Global_Sales"], labels=mlabels, autopct='%1.1f%%')
plt.legend()
plt.tight_layout()
right.pyplot(plt.figure(3))

# 6 Genre wise Average Sales
st.subheader("Genre wise average Sales")
cols = list(data.columns[6:])
op3 = st.multiselect(
    "Select Region ", data.columns[6:], default=cols)
result = data.groupby(['Genre']).mean()
st.bar_chart(result[op3], height=350, use_container_width=True)


# 7 Top 10 Stats
st.subheader("TOP 10 Games")
left, right = st.columns(2)

# 7.1 Top 10 Games by Platform
platform = sorted(data['Platform'].unique())
p = left.selectbox("Select platform", platform)
left.subheader("Top 10 Highest Grossing Games by platform")
df = data.query("Platform == @p")
df = df.sort_values(by=['Global_Sales'], ascending=False)
df = df.iloc[:10]
df = df[['Name', 'Global_Sales']]
left.table(df)

# 7.2 Top 10 Games by Genre
genre = sorted(data['Genre'].unique())
g = right.selectbox("Select genre", genre, index=6)
right.subheader("Top 10 Highest Grossing Games by genre")
df = data.query("Genre == @g")
df = df.sort_values(by=['Global_Sales'], ascending=False)
df = df.iloc[:10]
df = df[['Name', 'Global_Sales']]
right.table(df)

# 8 Comparing Sales Data of 2 PUblishers
st.subheader("Comparing Salesdata of two Publishers")
publisher = sorted(data['Publisher'].unique())
left, right = st.columns(2)
c1 = left.selectbox("Select 1st Publisher", publisher, index=21)
c2 = right.selectbox("Select 2nd Publisher", publisher, index=359)

df1 = data.query("Publisher == @c1")
df2 = data.query("Publisher == @c2")

group1 = df1.groupby("Year").sum()
group2 = df2.groupby("Year").sum()

fig, ax = plt.subplots(figsize=(width, height))

ax.bar(group1.index-0.2, group1['Global_Sales'], 0.4, label=c1, color="Red")
ax.bar(group2.index+0.2, group2['Global_Sales'],
       0.4, label=c2, color="orange")
ax.set_xlabel("Year")
ax.set_ylabel("Total Global Sales")
ax.legend()

st.pyplot(fig)


# Adding My credentials in sidebar
st.sidebar.write("Made by Harbir Singh")
