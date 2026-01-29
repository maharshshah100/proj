import base64    
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

import os
import requests
load_dotenv()

BACKEND_URL = "http://localhost:3001/api/auth"

# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(page_title="Diet Recommendation System", layout="centered")

# -------------------------------------------------------------------
# GLOBAL STYLES (YOUR ORIGINAL + AUTH STYLES ADDED)
# -------------------------------------------------------------------
def set_bg_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
 
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background:
                linear-gradient(145deg, rgba(19,23,32,0.85), rgba(28,34,48,0.85)),
                url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
 
# Call it
set_bg_image("images/img1.jpg")
 
st.markdown("""
<style>

/* ---------- AUTH CARD ---------- */
.auth-card {
    background: rgba(255,255,255,0.12);
    padding: 40px;
    border-radius: 22px;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.45);
    max-width: 450px;
    margin: auto;
}

.auth-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 900;
    color: white;
    margin-bottom: 10px;
}

.auth-subtitle {
    text-align: center;
    color: #cfcfcf;
    margin-bottom: 30px;
}

/* ---------- FORM CARD ---------- */
.form-card {
    background: rgba(255,255,255,0.10);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
}

/* Labels */
.stTextInput label, .stNumberInput label, .stSelectbox label {
    color: white !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
}

/* Inputs */
input, select, .stSelectbox > div {
    background: rgba(255,255,255,0.95) !important;
    color: black !important;
    border-radius: 12px !important;
}

/* Buttons */
.stButton > button {
    background: #00c853 !important;
    color: white !important;
    font-size: 1.1rem;
    font-weight: bold;
    padding: 12px;
    border-radius: 12px;
    width: 100%;
}
.stButton > button:hover {
    background: #009624 !important;
}

/* Markdown output fix */
.stMarkdown, .stMarkdown p, .stMarkdown li {
    color: white !important;
    line-height: 1.7;
}
.stMarkdown h3 {
    color: #00e676 !important;
    font-size: 1.9rem !important;
    margin-top: 30px;
}
.stMarkdown {
    background: rgba(0,0,0,0.35);
    padding: 25px;
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# LLM CONFIG
# -------------------------------------------------------------------
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

# -------------------------------------------------------------------
# PROMPT
# -------------------------------------------------------------------
prompt_template = PromptTemplate(
    input_variables=[
        "age","gender","weight","height",
        "veg_or_nonveg","disease","region",
        "allergies","foodtype","target_goal"
    ],
    template="""


USER PROFILE:
- Age: {age}
- Gender: {gender}
- Weight: {weight}
- Height: {height}
- Diet: {veg_or_nonveg}
- Medical condition: {disease}
- Region: {region}
- Allergies: {allergies}
- Food Type: {foodtype}
- Target Goal: {target_goal}

### 🥞 BREAKFAST
### 🍛 LUNCH
### 🍽 DINNER
### 🏋️ WORKOUT PLAN
### 💡 DIET TIPS
"""
)

chain = prompt_template | llm

# -------------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "auth"
if "users" not in st.session_state:
    st.session_state.users = {}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------------------------------------------------
# AUTH PAGE
# -------------------------------------------------------------------
if st.session_state.page == "auth":


    st.markdown("<div class='auth-title'>🥗 Diet Recommendation</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-subtitle'>Login or create your account</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            payload = {

            "email": email,

            "password": password

        }
 
        try:

            res = requests.post(f"{BACKEND_URL}/login", json=payload)
 
            if res.status_code == 200:

                st.session_state.logged_in = True

                st.session_state.page = "form"

                st.success("Login successful")

                st.rerun()

            else:

                st.error("Invalid credentials")
                
 
        except Exception as e:

            st.error("Backend not reachable")
 
 

    with tab2:
        su_username = st.text_input("Username ")
        su_email = st.text_input("Email",key="sign_email")
        su_fullname = st.text_input("Full Name")
        su_password = st.text_input("Password ", type="password")
        su_confirm = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            if su_password != su_confirm:
               st.error("Passwords do not match")

        else:

            payload = {

                "username": su_username,

                "email": su_email,

                "fullname": su_fullname,

                "password": su_password

            }
 
            try:

                res = requests.post(f"{BACKEND_URL}/save-user", json=payload)
 
                if res.status_code == 201:

                    st.success("Account created! Please login.")

                else:

                    st.error(res.json().get("message", "Signup failed"))
 
            except Exception as e:

                st.error("Backend not reachable")
 

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# FORM PAGE (UNCHANGED)
# -------------------------------------------------------------------
elif st.session_state.page == "form":

    st.markdown("<h1 style='text-align:center;'>🥗 Personalized Diet & Workout Plan</h1>", unsafe_allow_html=True)

    if st.button("🔙 Back to Login"):
        st.session_state.logged_in = False
        st.session_state.page = "auth"
        st.rerun()

    with st.form("diet_form"):
        

        age = st.number_input("Age", 1, 120, 25)
        gender = st.selectbox("Gender", ["male", "female", "other"])
        weight = st.number_input("Weight (kg)", 1, 300, 70)
        height = st.number_input("Height (cm)", 50, 250, 170)
        veg_or_nonveg = st.selectbox("Diet Preference", ["veg", "non-veg", "vegan"])
        disease = st.text_input("Any diseases", "none")
        region = st.text_input("Region", "India")
        allergies = st.text_input("Allergies", "none")
        foodtype = st.text_input("Food type", "balanced")
        target_goal = st.selectbox(
            "🎯 Target Goal",
            ["Weight Loss","Weight Gain","Muscle Building","General Fitness","Athletic Performance"]
        )

        submit = st.form_submit_button("Get Recommendations")
        st.markdown("</div>", unsafe_allow_html=True)

    if submit:
        st.session_state.user_data = {
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "veg_or_nonveg": veg_or_nonveg,
            "disease": disease,
            "region": region,
            "allergies": allergies,
            "foodtype": foodtype,
            "target_goal": target_goal
        }
        st.session_state.page = "result"
        st.rerun()

# -------------------------------------------------------------------
# RESULT PAGE (UNCHANGED)
# -------------------------------------------------------------------
elif st.session_state.page == "result":

    st.markdown("<h1 style='text-align:center;'>✨ Your Personalized Recommendation</h1>", unsafe_allow_html=True)

    with st.spinner("Generating plan..."):
        result = chain.invoke(st.session_state.user_data)

    st.markdown(result.content)

    if st.button("🔙 Go Back"):
        st.session_state.page = "form"
        st.rerun()
