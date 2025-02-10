import streamlit as st
import pandas as pd


# Load the dataset
@st.cache_data
def load_data():
    file_path = "preprocessed_data.csv"  # Ensure this file is in the repo
    return pd.read_csv(file_path)


data = load_data()

# Mapping of survey questions
q7_labels = {
    "Q7_1": "Choosing a concern or challenges for your project",
    "Q7_2": "Identifying participants for your project",
    "Q7_3": "Finding resources to use for your study",
    "Q7_4": "Choosing a strategy or action to try",
    "Q7_5": "Selecting data gathering tools",
    "Q7_6": "Defining how data analysis will work",
    "Q7_7": "Conducting the study",
    "Q7_8": "Analyzing data to find results",
    "Q7_9": "Presenting findings"
}

q9_labels = {
    "Q9_1": "Using the process tried in your study in your future classroom",
    "Q9_2": "Revisiting the AR/Inquiry process to solve future challenges in the classroom"
}


def filter_data(gender, age, cert_area, grad_date, research, q7_values, q9_values):
    filtered_data = data.copy()

    # Apply filters
    filters = {
        "gender": {"Any": None, "Male": 1, "Female": 0}.get(gender),
        "age": {"Any": None, "20-25 years old": 0, "26-40 years old": 1, "41+ years old": 9}.get(age),
        "certification_area": {"Any": None, "early childhood": 0, "elementary": 1, "high school": 2,
                               "middle school": 3}.get(cert_area),
        "grad_date": {"Any": None, "Dec-22": 0, "Dec-23": 1, "May-23": 2, "May-24": 3}.get(grad_date),
        "Q14": {"Any": None, "yes": 0, "no": 1}.get(research)
    }

    for key, value in filters.items():
        if value is not None:
            filtered_data = filtered_data[filtered_data[key] == value]

    for q_key, value in q7_values.items():
        if value != "Any":
            filtered_data = filtered_data[filtered_data[q_key] == float(value)]

    for q_key, value in q9_values.items():
        if value != "Any":
            filtered_data = filtered_data[filtered_data[q_key] == float(value)]

    return filtered_data


st.title("Survey Response Filter")

# Sidebar for Filters
st.sidebar.header("Filters")
gender = st.sidebar.selectbox("Gender", ["Any", "Male", "Female"])
age = st.sidebar.selectbox("Age", ["Any", "20-25 years old", "26-40 years old", "41+ years old"])
cert_area = st.sidebar.selectbox("Certification Area",
                                 ["Any", "early childhood", "elementary", "high school", "middle school"])
grad_date = st.sidebar.selectbox("Graduation Date", ["Any", "Dec-22", "Dec-23", "May-23", "May-24"])
research = st.sidebar.selectbox("Consent for Research", ["Any", "yes", "no"])

st.sidebar.subheader("Q7 Questions")
q7_values = {q: st.sidebar.selectbox(label, ["Any", "1", "2", "3", "4", "5"]) for q, label in q7_labels.items()}

st.sidebar.subheader("Q9 Questions")
q9_values = {q: st.sidebar.selectbox(label, ["Any", "1", "2", "3", "4", "5"]) for q, label in q9_labels.items()}

# Filter data
filtered_data = filter_data(gender, age, cert_area, grad_date, research, q7_values, q9_values)
st.write(f"### Number of responses: {len(filtered_data)}")

# Show filtered data
if not filtered_data.empty:
    st.dataframe(filtered_data)

# Response display
st.write("### View Responses")
for q in ['challenges you found in this process', 'what you learned about your students', 'impact of perception of yourself as a teacher', 'outcomes you found as a result of your study']:
    if st.button(f"Show Responses for {q}"):
        responses = "\n\n".join([f"Response {idx + 1}: {row[q]}" for idx, row in filtered_data.iterrows()])
        st.text_area(f"Responses for {q}", responses, height=300)
