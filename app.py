import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Pregnancy Risk Detector",
    page_icon="🤰",
    layout="wide"
)

# Clean black background with medical blue theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    .stApp {
        background: #0a0a0a;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Medical cross pattern overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.1) 2px, transparent 2px),
            radial-gradient(circle at 25% 25%, rgba(147, 197, 253, 0.1) 1px, transparent 1px);
        background-size: 50px 50px, 30px 30px;
        pointer-events: none;
        z-index: -1;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #111827;
        border-right: 2px solid #1e40af;
    }
    
    .sidebar-title {
        color: #3b82f6;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .sidebar-content {
        color: #d1d5db;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    .sidebar-stat {
        background: #1f2937;
        border-left: 3px solid #3b82f6;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .sidebar-stat-number {
        color: #3b82f6;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .sidebar-stat-label {
        color: #9ca3af;
        font-size: 0.8rem;
    }
    
    /* Main title styling */
    .main-title {
        text-align: center;
        margin: 2rem 0 1rem 0;
        color: #3b82f6;
        font-size: 3rem;
        font-weight: 600;
        text-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
    }
    
    .main-subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        line-height: 1.6;
    }
    
    /* Remove all backgrounds and borders */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 2px solid #374151;
        border-radius: 0;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        color: #9ca3af !important;
        font-weight: 500;
        padding: 1rem 2rem;
        border-bottom: 3px solid transparent !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #3b82f6 !important;
        border-bottom: 3px solid #3b82f6 !important;
        font-weight: 600;
    }
    
    /* Section titles */
    .section-title {
        color: #f3f4f6;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #374151;
    }
    
    /* Slider styling with blue theme */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #2563eb) !important;
    }
    
    .stSlider > div > div > div {
        background: #374151 !important;
    }
    
    .stSlider label {
        color: #d1d5db !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    /* Selectbox styling */
    .stSelectbox label {
        color: #d1d5db !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
    }
    
    .stSelectbox > div > div {
        background-color: #1f2937 !important;
        border: 2px solid #374151 !important;
        color: #f3f4f6 !important;
    }
    
    /* Button styling with blue theme */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 1rem 2rem;
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 2rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    }
    
    /* Result styling without boxes - keep original colors */
    .result-high {
        text-align: center;
        margin: 3rem 0;
        padding: 2rem 0;
        border-top: 3px solid #ef4444;
        border-bottom: 3px solid #ef4444;
    }
    
    .result-low {
        text-align: center;
        margin: 3rem 0;
        padding: 2rem 0;
        border-top: 3px solid #10b981;
        border-bottom: 3px solid #10b981;
    }
    
    .result-text {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px currentColor;
    }
    
    .result-description {
        font-size: 1.3rem;
        margin-bottom: 1.5rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with pregnancy awareness content
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤱 Maternal Health Insights</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #1f2937; border-radius: 12px; padding: 1.2rem; margin: 1rem 0; border: 1px solid #374151;">
        <div style="color: #60a5fa; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.8rem; display: flex; align-items: center;">
            🎯 Why Early Detection Matters
        </div>
        <div style="color: #e5e7eb; line-height: 1.6; font-size: 0.95rem;">
            Identifying pregnancy complications early can save lives and prevent serious health issues for both mother and baby.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-stat">
        <div class="sidebar-stat-number">295,000</div>
        <div class="sidebar-stat-label">Annual maternal deaths worldwide</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-stat">
        <div class="sidebar-stat-number">15%</div>
        <div class="sidebar-stat-label">Pregnancies develop complications</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-stat">
        <div class="sidebar-stat-number">85%</div>
        <div class="sidebar-stat-label">Complications are preventable</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #1f2937; border-radius: 12px; padding: 1.2rem; margin: 1rem 0; border: 1px solid #374151;">
        <div style="color: #f87171; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.8rem; display: flex; align-items: center;">
            ⚠️ Key Risk Factors
        </div>
        <div style="color: #e5e7eb; line-height: 1.8; font-size: 0.9rem;">
            • High blood pressure<br>
            • Diabetes (pre-existing or gestational)<br>
            • Previous pregnancy complications<br>
            • Extreme maternal age<br>
            • Mental health conditions<br>
            • Abnormal BMI levels
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #1f2937; border-radius: 12px; padding: 1.2rem; margin: 1rem 0; border: 1px solid #374151;">
        <div style="color: #34d399; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.8rem; display: flex; align-items: center;">
            💡 Prevention Tips
        </div>
        <div style="color: #e5e7eb; line-height: 1.8; font-size: 0.9rem;">
            • Regular prenatal check-ups<br>
            • Healthy diet and exercise<br>
            • Avoid smoking and alcohol<br>
            • Take prenatal vitamins<br>
            • Manage stress levels<br>
            • Monitor blood pressure
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    # Main title
    st.markdown("""
    <div class="main-title">🤰 Pregnancy Risk Detector</div>
    <div style="text-align: center; color: #9ca3af; font-size: 1.2rem; line-height: 1.5; max-width: 700px; margin: 0 auto;">
        <em><strong style="color: #3b82f6;">AI-Powered Screening</strong> for early detection of pregnancy risks, supporting smart choices for healthier maternal care.</em>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🩺 Vitals", "📊 Health Metrics", "📁 Medical History"])

    # === VITALS TAB ===
    with tab1:
        st.markdown('<div class="section-title">🩺 Vital Signs Monitoring</div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            age = st.slider("Age", min_value=10, max_value=65, value=30, key="age")
            systolic_bp = st.slider("Systolic BP", min_value=70.0, max_value=200.0, value=120.0, key="systolic")
            diastolic = st.slider("Diastolic BP", min_value=40.0, max_value=140.0, value=80.0, key="diastolic")
        
        with col_b:
            body_temp = st.slider("Body Temperature (°F)", min_value=97.0, max_value=103.0, value=98.6, key="temp")
            heart_rate = st.slider("Heart Rate (bpm)", min_value=58.0, max_value=92.0, value=75.0, key="heart")

    # === HEALTH METRICS TAB ===
    with tab2:
        st.markdown('<div class="section-title">🧬 Laboratory Results</div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            bs = st.slider("Blood Sugar", min_value=3.0, max_value=19.0, value=8.0, key="bs")
            bmi = st.slider("BMI", min_value=0.0, max_value=37.0, value=22.0, key="bmi")
        
        with col_b:
            mental_health = st.selectbox("Mental Health Condition?", ["No", "Yes"], key="mental")

    # === MEDICAL HISTORY TAB ===
    with tab3:
        st.markdown('<div class="section-title">📋 Clinical History</div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            prev_comp = st.selectbox("Previous Complications?", ["No", "Yes"], key="prev")
            pre_diabetes = st.selectbox("Preexisting Diabetes?", ["No", "Yes"], key="pre_dia")
        
        with col_b:
            gest_diabetes = st.selectbox("Gestational Diabetes?", ["No", "Yes"], key="gest_dia")

    # Convert yes/no to 0/1
    mental_health_val = 1 if mental_health == "Yes" else 0
    prev_comp_val = 1 if prev_comp == "Yes" else 0
    pre_diabetes_val = 1 if pre_diabetes == "Yes" else 0
    gest_diabetes_val = 1 if gest_diabetes == "Yes" else 0

    # Predict Button
    if st.button("🔬 Predict Risk Level"):
        try:
            # Load the model
            model = joblib.load("pregnancy_risk_detector.pkl")

            # Prepare input for model
            columns = ['Age', 'Systolic BP', 'Diastolic', 'BS', 'Body Temp', 'BMI',
                       'Previous Complications', 'Preexisting Diabetes', 'Gestational Diabetes',
                       'Mental Health', 'Heart Rate']

            input_df = pd.DataFrame([[age, systolic_bp, diastolic, bs, body_temp, bmi,
                                    prev_comp_val, pre_diabetes_val, gest_diabetes_val,
                                    mental_health_val, heart_rate]],
                                   columns=columns)

            prediction = model.predict(input_df)[0]

            # Display result without confidence level, bar, or explanations
            if prediction == 1:
                st.markdown(f"""
                <div class="result-high">
                    <div class="result-text" style="color: #ef4444;">🔴 HIGH RISK</div>
                    <div class="result-description" style="color: #fca5a5;">Your pregnancy is identified as high risk and needs prompt medical care.</div>
                    <p style="color: #f87171; margin-top: 2rem; font-size: 1.1rem;">
                        <em>🏥 Please consult your doctor promptly for the best care.</em>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-low">
                    <div class="result-text" style="color: #10b981;">🟢 LOW RISK</div>
                    <div class="result-description" style="color: #6ee7b7;">Your pregnancy is considered low risk at this time.</div>
                    <p style="color: #34d399; margin-top: 2rem; font-size: 1.1rem;">
                        <em>💚 Keep up with regular prenatal visits and maintain a healthy lifestyle.</em>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
        except FileNotFoundError:
            st.error("❌ Model file not found. Please ensure 'pregnancy_risk_detector.pkl' is available.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

with col2:
    # Empty space for balance
    st.write("")

# Footer
st.markdown("""
<div style="text-align: wide; color: #9ca3af; font-size: 0.9rem; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid #374151; line-height: 1.8;">
    <em>🔍 <strong>Disclaimer:</strong> This tool is for general awareness only and not a substitute for medical advice.</em><br>
    <em>📝 Note: Always speak with a qualified doctor or medical professional about your health.</em><br><br>
    <span style="font-size: 0.85rem; color: #6b7280;">
        © 2025 <strong>Pregnancy Risk Detector</strong> | Empowering maternal health through AI<br>
        <em>Built with ❤️ by Adeel Iqbal</em>
    </span>
</div>
""", unsafe_allow_html=True)
