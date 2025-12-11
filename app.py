# import streamlit as st
# import google.generativeai as genai
# st.title("Meal Planner")
# age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)
# weight = st.number_input("Enter your weight (kg):")
# height = st.number_input("Enter your height (cm):")
# location = st.text_input("Enter your location (city):")
# constraints = st.text_area("Enter any dietary constraints (e.g., vegetarian, gluten-free):")
# prompt = f"create a meal planner for a age {age}years old person and his weight is {weight}kg and height is {height} cm and he lives in {location} and he is {constraints}. you have to create a response as a table"
# if st.button("Generate Meal Plan"):
#     genai.configure(api_key = "AIzaSyC2G5CPS2pOQYjbgnruFsJVP-2_55dgrdo")
#     model = genai.GenerativeModel("gemini-2.5-flash")
#     response = model.generate_content(prompt)
#     st.write(response.text)


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.title("📚 Student Data Analysis Dashboard")
st.write("Learn data visualization with student performance data!")

# Create sample student data
np.random.seed(42)
n_students = 100

student_data = {
    "Student ID": range(1001, 1001 + n_students),
    "Name": [f"Student_{i}" for i in range(1, n_students + 1)],
    "Math Score": np.random.randint(40, 100, n_students),
    "English Score": np.random.randint(40, 100, n_students),
    "Science Score": np.random.randint(40, 100, n_students),
    "History Score": np.random.randint(40, 100, n_students),
    "Attendance (%)": np.random.randint(60, 100, n_students),
    "Grade": np.random.choice(["A", "B", "C", "D"], n_students, p=[0.2, 0.3, 0.35, 0.15]),
}

df = pd.DataFrame(student_data)
df["Average Score"] = df[["Math Score", "English Score", "Science Score", "History Score"]].mean(axis=1).round(2)

# Display sample data
st.subheader("📊 Sample Student Data")
st.dataframe(df.head(10), use_container_width=True)

st.write(f"Total Students: {len(df)}")

# Create tabs for different visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Score Distribution", "📊 Subject Comparison", "🎯 Average Scores", "📉 Attendance vs Performance", "🏆 Grade Distribution"])

with tab1:
    st.subheader("Score Distribution by Subject")
    fig = go.Figure()
    for subject in ["Math Score", "English Score", "Science Score", "History Score"]:
        fig.add_trace(go.Histogram(x=df[subject], name=subject, opacity=0.7))
    fig.update_layout(
        title="Distribution of Scores Across All Subjects",
        xaxis_title="Score",
        yaxis_title="Number of Students",
        barmode="overlay",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Average Score by Subject")
    subject_avg = {
        "Math": df["Math Score"].mean(),
        "English": df["English Score"].mean(),
        "Science": df["Science Score"].mean(),
        "History": df["History Score"].mean(),
    }
    fig = px.bar(
        x=list(subject_avg.keys()),
        y=list(subject_avg.values()),
        title="Average Performance by Subject",
        labels={"x": "Subject", "y": "Average Score"},
        color=list(subject_avg.values()),
        color_continuous_scale="Viridis"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Top 20 Students by Average Score")
    top_students = df.nlargest(20, "Average Score")[["Name", "Average Score", "Grade"]]
    fig = px.bar(
        top_students,
        y="Name",
        x="Average Score",
        title="Top 20 Performing Students",
        color="Average Score",
        color_continuous_scale="RdYlGn",
        orientation="h"
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Attendance vs Average Performance")
    fig = px.scatter(
        df,
        x="Attendance (%)",
        y="Average Score",
        color="Grade",
        size="Average Score",
        hover_name="Name",
        title="Correlation Between Attendance and Academic Performance",
        labels={"Attendance (%)": "Attendance Percentage", "Average Score": "Average Score"}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("Grade Distribution")
    grade_counts = df["Grade"].value_counts()
    fig = px.pie(
        values=grade_counts.values,
        names=grade_counts.index,
        title="Student Grade Distribution",
        hole=0.3
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# Summary statistics
st.subheader("📈 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Average Math Score", f"{df['Math Score'].mean():.1f}")
with col2:
    st.metric("Average English Score", f"{df['English Score'].mean():.1f}")
with col3:
    st.metric("Average Science Score", f"{df['Science Score'].mean():.1f}")
with col4:
    st.metric("Average Attendance", f"{df['Attendance (%)'].mean():.1f}%")

# Maximum Scored Subjects Pie Chart
st.subheader("🥇 Maximum Scored Subjects Distribution")
subject_scores = {
    "Math": df["Math Score"].mean(),
    "English": df["English Score"].mean(),
    "Science": df["Science Score"].mean(),
    "History": df["History Score"].mean(),
}

fig_pie = px.pie(
    values=list(subject_scores.values()),
    names=list(subject_scores.keys()),
    title="Subject Performance Distribution - Average Scores",
    color_discrete_sequence=px.colors.qualitative.Set2,
    hole=0.2
)
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
fig_pie.update_layout(height=500)
st.plotly_chart(fig_pie, use_container_width=True)

# Interactive filtering
st.subheader("🔍 Filter Students")
col1, col2 = st.columns(2)
with col1:
    min_score = st.slider("Minimum Average Score", 0, 100, 50)
with col2:
    selected_grade = st.multiselect("Select Grade(s)", df["Grade"].unique(), default=df["Grade"].unique())

filtered_df = df[(df["Average Score"] >= min_score) & (df["Grade"].isin(selected_grade))]
st.write(f"Showing {len(filtered_df)} students out of {len(df)}")
st.dataframe(filtered_df, use_container_width=True)


