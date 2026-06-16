import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Recruiter Sourcing Tool", page_icon="🔍", layout="wide")
st.title("🔍 GitHub Tech Talent Sourcing Tool")
st.write("Find top-rated coders sorted by impact score.")

col1, col2 = st.columns(2)
with col1:
    language = st.text_input("Programming Language", value="Python")
with col2:
    location = st.text_input("Region / Location", value="London")

if st.button("Search Candidates", type="primary"):
    with st.spinner("Scanning GitHub profiles... This takes a moment."):
        query = f"location:{location} language:{language}"
        url = f"https://api.github.com/search/users?q={query}&per_page=30"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                items = response.json().get("items", [])
                candidate_list = []
                
                for item in items:
                    detail_res = requests.get(item["url"])
                    if detail_res.status_code == 200:
                        user_data = detail_res.json()
                        followers = user_data.get("followers", 0)
                        repos = user_data.get("public_repos", 0)
                        score = (followers * 3) + repos
                        
                        candidate_list.append({
                            "Score": score,
                            "Name": user_data.get("name") or user_data.get("login"),
                            "Location": user_data.get("location"),
                            "Followers": followers,
                            "Public Repos": repos,
                            "GitHub Profile": user_data.get("html_url")
                        })
                
                if candidate_list:
                    df = pd.DataFrame(candidate_list).sort_values(by="Score", ascending=False)
                    st.success(f"Found {len(df)} candidates!")
                    st.dataframe(df, column_config={"GitHub Profile": st.column_config.LinkColumn("Open Profile")}, hide_index=True, use_container_width=True)
                else:
                    st.info("No developers found.")
            else:
                st.error("Rate limit reached. Try again in a few minutes!")
        except Exception as e:
            st.error(f"Error: {e}")
