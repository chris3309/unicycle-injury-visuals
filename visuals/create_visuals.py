# @Author: Chris Putzler
# @Date: 06-04-2025
# @Description: This script generates visualizations for unicycle injuries using the NEISS dataset.



import pandas as pd
import plotly.graph_objects as go
import plotly.express as px



#Loading the cleaned dataset from csv file
df = pd.read_csv("../data/NEISS_2005_2024_CLEAN.csv")
fmt = pd.read_csv("../data/NEISS_FMT.csv")




################## Chart 1: Line chart of injuries per year ##################
#Convert 'Treatment_Date' to datetime format
df["Treatment_Date"] = pd.to_datetime(df["Treatment_Date"], errors='coerce')

#Generate a new column for the year and extract year from 'Treatment_Date'
df["Year"] = df["Treatment_Date"].dt.year

#Count number of injuries per year
injuries_per_year = df["Year"].value_counts().sort_index().reset_index()
injuries_per_year.columns = ["Year", "Injuries"]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=injuries_per_year["Year"],
    y=injuries_per_year["Injuries"],
    mode='lines+markers',
    line=dict(color='#1f77b4', width=3),
    marker=dict(size=6),
    name='Injuries'
))

fig.update_layout(
    title="Unicycle Injuries Per Year (NEISS 2005–2024)",
    title_font_size=22,
    title_font_family="Arial",
    xaxis_title="Year",
    yaxis_title="Number of Injuries",
    xaxis=dict(showgrid=False, ticks='outside', tickfont=dict(size=12)),
    yaxis=dict(showgrid=True, gridcolor='lightgray', tickfont=dict(size=12)),
    plot_bgcolor='white',
    margin=dict(l=50, r=30, t=80, b=50),
    hovermode='x unified',
    font=dict(family="Segoe UI, sans-serif", size=14),
)

fig.write_html("number_of_injuries_over_time_line_chart.html")



################## Chart 2: Age Group Bar Chart ##################
bins = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ['0-4', '5-9', '10-14', '15-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
age_counts = df["Age_Group"].value_counts().sort_index()
fig_age = go.Figure()
fig_age.add_trace(go.Bar(
    x=age_counts.index.astype(str),
    y=age_counts.values,
    marker_color="#1f77b4"
))

fig_age.update_layout(
    title="Unicycle Injuries by Age Group",
    xaxis_title="Age Group",
    yaxis_title="Injuries",
    plot_bgcolor="white",
    showlegend=False,
    xaxis=dict(showgrid=False, tickfont=dict(size=12)),
    yaxis=dict(showgrid=True, gridcolor="lightgray", tickfont=dict(size=12)),
    font=dict(family="Segoe UI, sans-serif", size=14),
    margin=dict(l=40, r=30, t=60, b=50),
)
fig_age.write_html("unicycle_injuries_by_age_group_bar_chart.html")

################## Chart 3: Body Part Injuries Pie Chart ###################

# Extract body part mappings from NEISS_FMT
body_fmt = fmt[fmt["Format name"] == "BDYPT"]
body_fmt = body_fmt[["Starting value for format", "Format value label"]].dropna()
body_fmt.columns = ["Code", "Label"]
body_fmt["Code"] = body_fmt["Code"].astype(int)
body_fmt["Label"] = body_fmt["Label"].str.replace(r"^\d+\s*-\s*", "", regex=True).str.title()
# Create code-to-label mapping
code_to_label = dict(zip(body_fmt["Code"], body_fmt["Label"]))

# Map body part codes to labels
df["Body_Part_Label"] = df["Body_Part"].map(code_to_label)

# Count top 10 body parts
body_counts = df["Body_Part_Label"].value_counts().nlargest(10).reset_index()
body_counts.columns = ["Body Part", "Injuries"]


fig_body = px.pie(
    body_counts,
    names="Body Part",
    values="Injuries",
    title="Top 10 Body Parts Injured in Unicycle Accidents",
    hole=0.4
)

fig_body.update_traces(textposition='inside', textinfo='percent+label')
fig_body.update_layout(
    showlegend=True,
    font=dict(family="Segoe UI, sans-serif", size=14),
    margin=dict(l=40, r=40, t=60, b=40),
)


fig_body.write_html("unicycle_injuries_by_body_part_pie_chart.html")