import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

st.title("SHL Assessment Recommendation Engine")
st.write("Enter any job description or skills to get assessment recommendations.")

query = st.text_area("Job Description", height=150)

if st.button("Recommend"):
    if not query.strip():
        st.error("Please enter a job description.")
    else:
        with st.spinner("Fetching recommendations..."):
            response = requests.post(API_URL, json={"query": query})
            
            if response.status_code == 200:
                data = response.json()
                results = data["recommended_assessments"]

                if len(results) == 0:
                    st.warning("No recommendations found.")
                else:
                    st.success(f"Found {len(results)} recommended assessments")

                    # Formatting table
                    for item in results:
                        st.write("---")
                        st.subheader(item["name"])
                        st.write(f"**Description:** {item['description']}")
                        st.write(f"**URL:** {item['url']}")
                        st.write(f"**Test Type:** {item['test_type']}")
                        st.write(f"**Adaptive Support:** {item['adaptive_support']}")
                        st.write(f"**Remote Support:** {item['remote_support']}")
                        st.write(f"**Duration:** {item['duration']} min")
            else:
                st.error("API error. Please make sure the backend is running.")
