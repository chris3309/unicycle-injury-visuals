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

################## Chart 4: Injuries by Gender Pie Chart ###################

sex_fmt = fmt[fmt["Format name"] == "SEX"]
sex_fmt = sex_fmt[["Starting value for format", "Format value label"]].dropna()
sex_fmt.columns = ["Code", "Label"]
sex_fmt["Code"] = sex_fmt["Code"].astype(int)
sex_fmt["Label"] = sex_fmt["Label"].str.replace(r"^\d+\s*-\s*", "", regex=True).str.title()

code_to_label = dict(zip(sex_fmt["Code"], sex_fmt["Label"]))
df["Sex_Label"] = df["Sex"].map(code_to_label)

sex_counts = df["Sex_Label"].value_counts().reset_index()
sex_counts.columns = ["Sex", "Injuries"]

fig = px.pie(
    sex_counts,
    names="Sex",
    values="Injuries",
    title="Unicycle Injuries by Sex",
    hole=0.4
)
fig.update_traces(textposition="inside", textinfo="percent+label")
fig.update_layout(
    font=dict(family="Segoe UI, sans-serif", size=14),
    margin=dict(l=40, r=40, t=60, b=40),
)

fig.write_html("injuries_by_sex.html")


################## Chart 5: Injuries by Race Pie Chart ###################
# Extract and clean race labels
race_fmt = fmt[fmt["Format name"] == "RACE"]
race_fmt = race_fmt[["Starting value for format", "Format value label"]].dropna()
race_fmt.columns = ["Code", "Label"]
race_fmt["Code"] = race_fmt["Code"].astype(int)
race_fmt["Label"] = race_fmt["Label"].str.replace(r"^\d+\s*-\s*", "", regex=True).str.title()

# Map labels
code_to_label = dict(zip(race_fmt["Code"], race_fmt["Label"]))
df["Race_Label"] = df["Race"].map(code_to_label)
df = df[df["Race_Label"]!="N.S."]
# Count injuries by race
race_counts = df["Race_Label"].value_counts().reset_index()
race_counts.columns = ["Race", "Injuries"]

# Create donut chart
fig = px.pie(
    race_counts,
    names="Race",
    values="Injuries",
    title="Unicycle Injuries by Race",
    hole=0.4
)
fig.update_traces(textposition="inside", textinfo="percent+label")
fig.update_layout(
    font=dict(family="Segoe UI, sans-serif", size=14),
    margin=dict(l=40, r=40, t=60, b=40),
)

fig.write_html("injuries_by_race.html")



################## Chart 6: Injuries by Diagnosis ###################
#Extract and clean diagnosis labels
diag_fmt = fmt[fmt["Format name"] == "DIAG"]
diag_fmt = diag_fmt[["Starting value for format", "Format value label"]].dropna()
diag_fmt.columns = ["Code", "Label"]
diag_fmt["Code"] = diag_fmt["Code"].astype(int)
diag_fmt["Label"] = diag_fmt["Label"].str.replace(r"^\d+\s*-\s*", "", regex=True).str.title()

#Map labels
diagnosis_map = dict(zip(diag_fmt["Code"], diag_fmt["Label"]))
df["Diagnosis_Label"] = df["Diagnosis"].map(diagnosis_map)

#Count top diagnoses
diagnosis_counts = df["Diagnosis_Label"].value_counts().reset_index()
diagnosis_counts.columns = ["Diagnosis", "Injuries"]

#Plot diagnosis pie chart
fig_diag = px.pie(
    diagnosis_counts,
    names="Diagnosis",
    values="Injuries",
    title="Unicycle Injuries by Diagnosis",
    hole=0.4
)
fig_diag.update_traces(textposition="inside", textinfo="percent+label")
fig_diag.update_layout(
    font=dict(family="Segoe UI, sans-serif", size=14),
    margin=dict(l=40, r=40, t=60, b=40),
)
fig_diag.write_html("injuries_by_diagnosis.html")

################### Chart 7: Injuries by Disposition ###################

#Extract and clean disposition labels
disp_fmt = fmt[fmt["Format name"] == "DISP"]
disp_fmt = disp_fmt[["Starting value for format", "Format value label"]].dropna()
disp_fmt.columns = ["Code", "Label"]
disp_fmt["Code"] = disp_fmt["Code"].astype(int)
disp_fmt["Label"] = disp_fmt["Label"].str.replace(r"^\d+\s*-\s*", "", regex=True).str.title()

#Map labels
disposition_map = dict(zip(disp_fmt["Code"], disp_fmt["Label"]))
df["Disposition_Label"] = df["Disposition"].map(disposition_map)

#Count dispositions
disposition_counts = df["Disposition_Label"].value_counts().reset_index()
disposition_counts.columns = ["Disposition", "Injuries"]

#Plot disposition pie chart
fig_disp = px.pie(
    disposition_counts,
    names="Disposition",
    values="Injuries",
    title="Unicycle Injuries by Disposition",
    hole=0.4
)
fig_disp.update_traces(textposition="inside", textinfo="percent+label")
fig_disp.update_layout(
    font=dict(family="Segoe UI, sans-serif", size=14),
    margin=dict(l=40, r=40, t=60, b=40),
)
fig_disp.write_html("injuries_by_disposition.html")
