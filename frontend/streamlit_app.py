import json
import requests
import streamlit as st
from datetime import datetime
import pandas as pd

# Configure Streamlit
st.set_page_config(
    page_title="WorkWise Noesis - AI Career Copilot", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .gradient-text {
        background: linear-gradient(45deg, #ff6b6b, #ffa500, #ffff00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .skill-tag {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid rgba(34, 197, 94, 0.3);
        display: inline-block;
        margin: 0.25rem;
    }
    
    .gap-card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .tab-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .tab-button {
        padding: 1rem 2rem;
        background: transparent;
        border: none;
        color: #a0a0a0;
        cursor: pointer;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .tab-button.active {
        color: #ff6b6b;
        border-bottom-color: #ff6b6b;
    }
    
    .tab-button:hover {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'upload'
if 'api_base' not in st.session_state:
    st.session_state.api_base = 'http://localhost:8000'
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

def render_header():
    st.markdown("""
    <div class="main-header">
        <div style="text-align: center;">
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                <div style="width: 60px; height: 60px; background: linear-gradient(45deg, #ff6b6b, #ffa500); border-radius: 15px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                    <span style="color: white; font-size: 24px;">🚀</span>
                </div>
                <div>
                    <h1 style="font-size: 3rem; font-weight: bold; margin: 0;" class="gradient-text">WorkWise Noesis</h1>
                    <p style="color: #a0a0a0; margin: 0; font-size: 1.1rem;">AI-powered career and learning copilot for skill gap analysis and personalized upskilling roadmaps</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_tabs():
    tabs = [
        {'id': 'upload', 'name': '📄 Upload Resume', 'icon': 'fas fa-file-upload'},
        {'id': 'analysis', 'name': '📊 Analysis Results', 'icon': 'fas fa-chart-bar'},
        {'id': 'career', 'name': '🔍 Career Explorer', 'icon': 'fas fa-search'},
        {'id': 'stem', 'name': '🧪 STEM Explorer', 'icon': 'fas fa-flask'},
        {'id': 'chat', 'name': '💬 Chat Assistant', 'icon': 'fas fa-comments'},
        {'id': 'game', 'name': '🎮 Game Mode', 'icon': 'fas fa-gamepad'}
    ]
    
    cols = st.columns(len(tabs))
    for i, tab in enumerate(tabs):
        with cols[i]:
            if st.button(tab['name'], key=f"tab_{tab['id']}", 
                       help=f"Switch to {tab['name']}"):
                st.session_state.active_tab = tab['id']
                st.rerun()

def render_upload_tab():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    st.markdown("### 📄 Upload Your PDF Resume")
    st.markdown("Get AI-powered skill analysis and personalized career guidance")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type=['pdf'], 
        help="Upload your resume in PDF format"
    )
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Additional information
        st.markdown("### 📝 Additional Information (Optional)")
        additional_info = st.text_area(
            "Add any additional skills, experience, or goals you'd like to include in the analysis...",
            height=100,
            placeholder="e.g., I'm interested in machine learning and have completed several online courses..."
        )
        
        # Analyze button
        if st.button("🔮 Analyze Resume", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your resume..."):
                try:
                    # Upload PDF
                    files = {'file': uploaded_file}
                    data = {'additional_info': additional_info} if additional_info else {}
                    
                    upload_response = requests.post(
                        f"{st.session_state.api_base}/upload-pdf",
                        files=files,
                        data=data,
                        timeout=30
                    )
                    
                    if upload_response.ok:
                        upload_result = upload_response.json()
                        
                        # Analyze the extracted text
                        analysis_payload = {
                            'goal': 'Data Analyst',  # Default, can be made dynamic
                            'known_skills': upload_result.get('extracted_skills', []),
                            'resume_text': upload_result.get('text', '')
                        }
                        
                        analysis_response = requests.post(
                            f"{st.session_state.api_base}/analyze",
                            json=analysis_payload,
                            timeout=30
                        )
                        
                        if analysis_response.ok:
                            st.session_state.analysis_result = analysis_response.json()
                            st.session_state.active_tab = 'analysis'
                            st.success("🎉 Analysis complete! Switching to results...")
                            st.rerun()
                        else:
                            st.error(f"Analysis failed: {analysis_response.status_code}")
            else:
                        st.error(f"Upload failed: {upload_response.status_code}")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_analysis_tab():
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        
        # Extracted Skills
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ✅ Your Known Skills")
        if result.get('extracted_skills'):
            skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in result['extracted_skills']])
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.info("No skills extracted from resume")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Required Skills
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Required Skills for Target Role")
        if result.get('required_skills'):
            skills_html = "".join([f'<span class="skill-tag" style="background: rgba(59, 130, 246, 0.2); color: #3b82f6; border-color: rgba(59, 130, 246, 0.3);">{skill}</span>' for skill in result['required_skills']])
            st.markdown(skills_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Skill Gaps
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚠️ Skill Gaps Analysis")
        if result.get('skill_gaps'):
            for gap in result['skill_gaps']:
                status_color = "#22c55e" if gap['status'] == 'Known' else "#ef4444"
                status_bg = "rgba(34, 197, 94, 0.2)" if gap['status'] == 'Known' else "rgba(239, 68, 68, 0.2)"
                
                st.markdown(f"""
                <div class="gap-card">
                    <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 1rem;">
                        <h4 style="margin: 0; font-size: 1.2rem; color: white;">{gap['skill']}</h4>
                        <span style="background: {status_bg}; color: {status_color}; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.875rem; margin-left: auto;">{gap['status']}</span>
                    </div>
                    <p style="color: #a0a0a0; margin: 0.5rem 0;"><strong>Current Level:</strong> {gap['proficiency_level']} → <strong>Target:</strong> {gap['required_proficiency']}</p>
                    <p style="color: #a0a0a0; margin: 0.5rem 0;"><strong>Reasoning:</strong> {gap['reasoning']}</p>
                    <p style="color: #a0a0a0; margin: 0.5rem 0;"><strong>Recommendation:</strong> {gap['recommendation']}</p>
                    <div style="margin-top: 1rem; font-size: 0.875rem; color: #6b7280;">
                        <span style="margin-right: 1rem;">Mastery Points: {gap['mastery_points']}</span>
                        <span style="margin-right: 1rem;">Current Score: {gap['current_score']}</span>
                        <span>Required Score: {gap['required_score']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
                        
                else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 No Analysis Available")
        st.info("Upload and analyze a resume to see results here")
        st.markdown('</div>', unsafe_allow_html=True)

def render_career_tab():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Career Explorer")
    st.markdown("**Coming Soon:** Connect with employers and find suitable job opportunities")
    st.markdown('</div>', unsafe_allow_html=True)

def render_stem_tab():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🧪 STEM Explorer")
    st.markdown("**Coming Soon:** Find ideal majors, AI takeover risks, and career paths")
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat_tab():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💬 Chat Assistant")
    st.markdown("**Coming Soon:** AI-powered conversational assistance for your career journey")
    st.markdown('</div>', unsafe_allow_html=True)

def render_game_tab():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎮 Game Mode")
    st.markdown("**Coming Soon:** Gamified learning with courses, points, stages, and boss levels")
    st.markdown('</div>', unsafe_allow_html=True)

# Main app
def main():
    render_header()
    render_tabs()
    
    # Render active tab content
    if st.session_state.active_tab == 'upload':
        render_upload_tab()
    elif st.session_state.active_tab == 'analysis':
        render_analysis_tab()
    elif st.session_state.active_tab == 'career':
        render_career_tab()
    elif st.session_state.active_tab == 'stem':
        render_stem_tab()
    elif st.session_state.active_tab == 'chat':
        render_chat_tab()
    elif st.session_state.active_tab == 'game':
        render_game_tab()
    
    # Sidebar settings
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        api_base = st.text_input("API Base URL", value=st.session_state.api_base)
        st.session_state.api_base = api_base
        
        # Health check
        if st.button("🔍 Check API Health"):
            try:
                response = requests.get(f"{api_base}/health", timeout=5)
                if response.ok:
                    st.success("✅ API is healthy")
                else:
                    st.error(f"❌ API error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ API unreachable: {e}")

if __name__ == "__main__":
    main()