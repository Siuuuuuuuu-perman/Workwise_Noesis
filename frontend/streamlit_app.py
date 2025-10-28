import json
import requests
import streamlit as st

st.set_page_config(page_title="Noesis - Learning Gap Assistant", layout="wide")
st.title("Noesis — Enhanced AI Learning Gap Solution")

with st.sidebar:
    st.header("User Settings")
    api_base = st.text_input("API Base URL", value=st.session_state.get("api_base", "http://localhost:8000"))
    st.session_state["api_base"] = api_base
    
    # Role selection with STEM options
    try:
        r = requests.get(f"{api_base}/roles", timeout=5)
        if r.ok:
            roles_data = r.json()["roles"]
            role_options = [f"{role['name']} ({role['category']})" for role in roles_data]
            selected_role = st.selectbox("Target Role", role_options, index=0)
            goal = selected_role.split(" (")[0]  # Extract just the role name
        else:
            goal = st.text_input("Target Role", value="Data Analyst")
    except:
        goal = st.text_input("Target Role", value="Data Analyst")
    
    weekly_hours = st.number_input("Weekly Time (hours)", min_value=1, max_value=40, value=5)
    free_preferred = st.checkbox("Prefer Free Resources", value=True)
    provider_prefs = st.multiselect("Preferred Providers", ["Coursera", "edX", "Udemy", "Khan Academy"]) 
    
    # Quick health check
    if st.button("Check API"):
        try:
            r = requests.get(f"{api_base}/health", timeout=5)
            if r.ok:
                st.success("API reachable")
            else:
                st.error(f"API error: {r.status_code}")
        except Exception as e:
            st.error(f"API unreachable: {e}")

st.subheader("1) Provide Background")
known_skills = st.text_input("Known Skills (comma-separated)")

# PDF Upload Section
st.write("**Upload PDF Resume (converts to XML):**")
uploaded_pdf = st.file_uploader("Upload PDF Resume", type=["pdf"], accept_multiple_files=False, key="pdf_uploader")

# Traditional text input
st.write("**Or enter text manually:**")
uploaded_txt = st.file_uploader("Upload TXT Resume", type=["txt"], accept_multiple_files=False, key="txt_uploader")
resume_text_manual = st.text_area("Resume / Background Text (optional)", height=160)

def extract_text_from_upload(file):
    if file is None:
        return ""
    name = (file.name or "").lower()
    if name.endswith(".txt"):
        try:
            return file.read().decode("utf-8", errors="ignore")
        except Exception:
            file.seek(0)
            return file.read().decode("latin-1", errors="ignore")
    st.warning("Unsupported file type; please upload TXT.")
    return ""

# Handle PDF upload and XML conversion
xml_content = ""
resume_text = ""

if uploaded_pdf is not None:
    st.info("🔄 Converting PDF to XML format...")
    try:
        # Upload PDF to backend for XML conversion
        files = {"file": uploaded_pdf}
        r = requests.post(f"{st.session_state['api_base']}/upload-pdf", files=files, timeout=30)
        if r.ok:
            result = r.json()
            xml_content = result["xml_content"]
            resume_text = result["text_content"]
            st.success(f"✅ PDF converted to XML: {result['filename']}")
            st.session_state["xml_content"] = xml_content
            st.session_state["pdf_filename"] = result["filename"]
            
            # Show XML preview
            with st.expander("📄 View XML Structure"):
                st.code(xml_content, language="xml")
        else:
            st.error(f"PDF conversion failed: {r.text}")
    except Exception as e:
        st.error(f"Error uploading PDF: {e}")

# Handle TXT upload
elif uploaded_txt is not None:
    resume_text = extract_text_from_upload(uploaded_txt)
    if resume_text:
        st.success("✅ TXT file processed")

# Combine with manual text
if resume_text_manual:
    resume_text = (resume_text + "\n" + resume_text_manual).strip()

if isinstance(known_skills, str):
    known_skills_list = [s.strip() for s in known_skills.split(",") if s.strip()]
else:
    known_skills_list = known_skills

col1, col2 = st.columns(2)
with col1:
    if st.button("Analyze Skills"):
        if xml_content and "xml_content" in st.session_state:
            # Use XML analysis for PDF uploads
            try:
                data = {
                    "xml_content": st.session_state["xml_content"],
                    "goal": goal,
                    "weekly_time_hours": weekly_hours
                }
                r = requests.post(f"{st.session_state['api_base']}/analyze-xml", data=data, timeout=20)
                if r.ok:
                    result = r.json()
                    st.session_state["analyze"] = {
                        "extracted_skills": result["extracted_skills"],
                        "required_skills": result["required_skills"],
                        "skill_gaps": result["skill_gaps"]
                    }
                    st.success("✅ Skills analyzed from XML format")
                else:
                    st.error(f"XML analysis failed: {r.text}")
            except Exception as e:
                st.error(f"Error analyzing XML: {e}")
        else:
            # Use regular text analysis
            payload = {
                "name": "User",
                "goal": goal,
                "known_skills": known_skills_list,
                "weekly_time_hours": weekly_hours,
                "resume_text": resume_text,
            }
            try:
                r = requests.post(f"{st.session_state['api_base']}/analyze", json=payload, timeout=20)
            except Exception as e:
                st.error(f"Failed to reach API: {e}")
                r = None
            if r and r.ok:
                st.session_state["analyze"] = r.json()
            else:
                st.error(r.text if r is not None else "No response from API")

if "analyze" in st.session_state:
    st.subheader("🎯 Skill Gap Analysis")
    data = st.session_state["analyze"]
    
    # Enhanced skill gap visualization
    st.markdown("### 📊 Current vs Required Proficiency")
    
    for gap in data["skill_gaps"]:
        with st.expander(f"🔧 {gap['skill'].title()} - {gap['status']}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Level", gap.get('proficiency_level', 'Unknown'))
                st.metric("Current Score", f"{gap.get('current_score', 0):.1%}")
            
            with col2:
                st.metric("Required Level", gap.get('required_proficiency', 'Unknown'))
                st.metric("Required Score", f"{gap.get('required_score', 0):.1%}")
            
            with col3:
                progress = gap.get('current_score', 0) / max(gap.get('required_score', 1), 0.1)
                st.metric("Progress", f"{min(progress, 1):.1%}")
                st.metric("Mastery Points", f"{gap.get('mastery_points', 0)}")
            
            # Progress bar
            progress_value = min(gap.get('current_score', 0) / max(gap.get('required_score', 1), 0.1), 1.0)
            st.progress(progress_value)
            
            # Reasoning
            st.markdown(f"**💡 Why this skill matters:** {gap.get('reasoning', 'Essential for the role')}")
            
            # Recommendation
            st.markdown(f"**🎯 Next steps:** {gap.get('recommendation', 'Start learning this skill')}")
    
    # Summary metrics
    st.markdown("### 📈 Learning Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    total_skills = len(data["skill_gaps"])
    known_skills = len([g for g in data["skill_gaps"] if g.get('status') == 'Known'])
    missing_skills = len([g for g in data["skill_gaps"] if g.get('status') == 'Missing'])
    total_mastery_points = sum([g.get('mastery_points', 0) for g in data["skill_gaps"]])
    
    with col1:
        st.metric("Total Skills", total_skills)
    with col2:
        st.metric("Known Skills", known_skills)
    with col3:
        st.metric("Missing Skills", missing_skills)
    with col4:
        st.metric("Total Mastery Points", total_mastery_points)

    st.subheader("2) Initial Assessment")
    missing_skills = [g["skill"] for g in data["skill_gaps"] if g["status"].lower() != "known"]
    if st.button("Generate Assessment"):
        try:
            r = requests.post(f"{st.session_state['api_base']}/assessment/generate", json={"skills": missing_skills, "num_questions_per_skill": 2}, timeout=20)
        except Exception as e:
            st.error(f"Failed to reach API: {e}")
            r = None
        if r and r.ok:
            st.session_state["questions"] = r.json()["questions"]
        else:
            st.error(r.text if r is not None else "No response from API")

    if "questions" in st.session_state:
        st.write("Answer the questions:")
        responses = []
        for q in st.session_state["questions"]:
            idx = st.radio(q["prompt"], options=list(range(len(q["options"]))), format_func=lambda i: q["options"][i], key=q["id"])
            responses.append({"id": q["id"], "skill": q["skill"], "selected_index": idx, "answer_index": q["answer_index"]})
        if st.button("Submit Assessment"):
            try:
                r = requests.post(f"{st.session_state['api_base']}/assessment/submit", json={"responses": responses}, timeout=20)
            except Exception as e:
                st.error(f"Failed to reach API: {e}")
                r = None
            if r and r.ok:
                st.session_state["assessment_result"] = r.json()
            else:
                st.error(r.text if r is not None else "No response from API")

    if "assessment_result" in st.session_state:
        res = st.session_state["assessment_result"]
        st.write(res["results"])
        # Update known skills with assessment
        enhanced_known = sorted(set(data["extracted_skills"]) | set(res.get("updated_known_skills", [])))
        st.session_state["enhanced_known_skills"] = enhanced_known
        st.success(f"Updated known skills: {', '.join(enhanced_known)}")

        st.subheader("3) Resource Recommendations")
        refined_missing = [s for s in data["required_skills"] if s.lower() not in [k.lower() for k in enhanced_known]]
        try:
            r = requests.post(
            f"{st.session_state['api_base']}/resources",
            json={
                "missing_skills": refined_missing,
                "weekly_time_hours": weekly_hours,
                "free_preferred": free_preferred,
                "provider_preferences": provider_prefs,
            }, timeout=20,
        )
        except Exception as e:
            st.error(f"Failed to reach API: {e}")
            r = None
        if r and r.ok:
            ranked = r.json()["resources"]
            st.session_state["ranked_resources"] = ranked
            st.table(ranked)
        else:
            st.error(r.text if r is not None else "No response from API")

        st.subheader("4) 🎮 Gamified Learning Roadmap")
        if "ranked_resources" in st.session_state and st.button("Generate Gamified Roadmap"):
            try:
                r = requests.post(
                f"{st.session_state['api_base']}/roadmap",
                json={
                    "goal": goal,
                    "missing_skills": refined_missing,
                    "weekly_time_hours": weekly_hours,
                    "ranked_resources": st.session_state["ranked_resources"],
                    "weeks": 6,
                }, timeout=20,
            )
            except Exception as e:
                st.error(f"Failed to reach API: {e}")
                r = None
            if r and r.ok:
                plan = r.json()["learning_roadmap"]
                st.session_state["roadmap"] = plan
                
                # Display gamified roadmap
                st.markdown("### 🏆 Your Learning Journey")
                
                total_mastery_points = 0
                for entry in plan:
                    with st.expander(f"Week {entry['week']}: {entry['topic']}", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"**📚 Resource:** {entry['resource']}")
                            st.markdown(f"**⏱️ Time:** {entry['hours']} hours")
                        
                        with col2:
                            st.markdown(f"**🎯 Goal:** {entry['goal']}")
                        
                        with col3:
                            # Extract mastery points from goal
                            import re
                            points_match = re.search(r'(\d+) mastery points', entry['goal'])
                            points = int(points_match.group(1)) if points_match else 50
                            total_mastery_points += points
                            st.metric("Mastery Points", points)
                
                st.markdown(f"### 🏅 Total Mastery Points Available: {total_mastery_points}")
                
                # Real-world problems section
                st.markdown("### 🧩 Real-World Problem Solving")
                if st.button("Get Practice Problems"):
                    try:
                        r = requests.post(
                            f"{st.session_state['api_base']}/problems/generate",
                            data={
                                "skills": refined_missing,
                                "role": goal.lower().replace(" ", "_"),
                                "difficulty": "intermediate"
                            }
                        )
                        if r.ok:
                            problems = r.json()["problems"]
                            st.session_state["problems"] = problems
                            
                            for i, problem in enumerate(problems):
                                with st.expander(f"Problem {i+1}: {problem['title']} ({problem['points']} points)", expanded=False):
                                    st.markdown(f"**📋 Description:** {problem['description']}")
                                    st.markdown(f"**🎯 Scenario:** {problem['scenario']}")
                                    st.markdown(f"**📊 Data Provided:** {problem['data_provided']}")
                                    
                                    st.markdown("**📝 Deliverables:**")
                                    for deliverable in problem['deliverables']:
                                        st.markdown(f"- {deliverable}")
                                    
                                    st.markdown("**💡 Hints:**")
                                    for hint in problem['hints']:
                                        st.markdown(f"- {hint}")
                                    
                                    if st.button(f"Start Problem {i+1}", key=f"start_problem_{i}"):
                                        st.session_state["current_problem"] = problem
                                        st.success(f"Started: {problem['title']}")
                        else:
                            st.error("Failed to generate problems")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error(r.text if r is not None else "No response from API")

# New Analysis Interfaces
if "analyze" in st.session_state:
    st.markdown("---")
    st.subheader("🤖 AI Replacement Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Analyze AI Replacement Risk"):
            try:
                data = st.session_state["analyze"]
                skills = data["extracted_skills"]
                r = requests.post(
                    f"{st.session_state['api_base']}/ai-analysis",
                    data={"role": goal, "skills": skills}
                )
                if r.ok:
                    ai_analysis = r.json()
                    st.session_state["ai_analysis"] = ai_analysis
                    
                    # Display AI risk analysis
                    st.markdown("### 🚨 AI Replacement Risk Assessment")
                    
                    risk_level = ai_analysis["risk_level"]
                    risk_color = "🔴" if risk_level == "High" else "🟡" if risk_level == "Medium" else "🟢"
                    st.metric("Overall Risk Level", f"{risk_color} {risk_level}")
                    st.metric("Risk Score", f"{ai_analysis['overall_risk']:.1%}")
                    
                    # Skill-level risks
                    st.markdown("#### Skill-Level Risk Analysis")
                    for skill_risk in ai_analysis["skill_risks"]:
                        risk_icon = "🔴" if skill_risk["risk"] == "High" else "🟡" if skill_risk["risk"] == "Medium" else "🟢"
                        st.write(f"{risk_icon} **{skill_risk['skill']}**: {skill_risk['risk']} risk")
                    
                    # Research citations
                    st.markdown("#### 📚 Research Citations")
                    for paper in ai_analysis["research_papers"]:
                        with st.expander(f"{paper['title']} ({paper['year']})"):
                            st.write(f"**Authors:** {paper['authors']}")
                            st.write(f"**Journal:** {paper['journal']}")
                            st.write(f"**Key Findings:** {paper['key_findings']}")
                            st.write(f"**URL:** {paper['url']}")
                    
                    # Strategies
                    st.markdown("#### 🛡️ AI Resistance Strategies")
                    for strategy in ai_analysis["strategies"]:
                        st.write(f"• {strategy}")
                        
                else:
                    st.error("Failed to analyze AI replacement risk")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        if st.button("Analyze Job Market"):
            try:
                data = st.session_state["analyze"]
                skills = data["extracted_skills"]
                r = requests.post(
                    f"{st.session_state['api_base']}/job-market",
                    data={"role": goal, "skills": skills}
                )
                if r.ok:
                    job_analysis = r.json()
                    st.session_state["job_analysis"] = job_analysis
                    
                    # Display job market analysis
                    st.markdown("### 💼 Job Market Analysis")
                    
                    market_data = job_analysis["market_data"]
                    st.metric("Total Jobs Available", f"{market_data['total_jobs']:,}")
                    st.metric("Growth Rate", f"{market_data['growth_rate']*100:.1f}%")
                    st.metric("Average Salary", f"${market_data['avg_salary']:,}")
                    st.metric("Competition Level", market_data["competition_level"])
                    
                    # Skill match
                    st.metric("Skill Match", f"{job_analysis['skill_match_percentage']:.1f}%")
                    st.metric("Job Likelihood", f"{job_analysis['job_likelihood']:.1%}")
                    
                    # Recommendations
                    st.markdown("#### 📈 Market Recommendations")
                    for rec in job_analysis["recommendations"]:
                        st.write(f"• {rec}")
                        
                else:
                    st.error("Failed to analyze job market")
            except Exception as e:
                st.error(f"Error: {e}")

# Interview Preparation Section
if "analyze" in st.session_state:
    st.markdown("---")
    st.subheader("🎤 Interview Preparation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Get Technical Questions"):
            try:
                r = requests.get(f"{st.session_state['api_base']}/interview-questions/{goal.lower().replace(' ', '_')}")
                if r.ok:
                    interview_data = r.json()
                    st.session_state["interview_questions"] = interview_data
                    
                    # Display technical questions
                    st.markdown("#### 🔧 Technical Interview Questions")
                    for i, question in enumerate(interview_data.get("technical", [])):
                        with st.expander(f"Question {i+1}: {question['question']} ({question['difficulty']})"):
                            st.write(f"**Category:** {question['category']}")
                            st.write(f"**Sample Answer:** {question['sample_answer']}")
                            st.write(f"**Follow-up:** {question['follow_up']}")
                            st.write("**Key Points:**")
                            for point in question['key_points']:
                                st.write(f"• {point}")
                else:
                    st.error("Failed to get interview questions")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        if st.button("Get Soft Skills Assessment"):
            try:
                r = requests.post(f"{st.session_state['api_base']}/assessment/soft-skills")
                if r.ok:
                    soft_skills_data = r.json()
                    st.session_state["soft_skills_questions"] = soft_skills_data["questions"]
                    
                    # Display soft skills questions
                    st.markdown("#### 🤝 Soft Skills Assessment")
                    for i, question in enumerate(soft_skills_data["questions"][:3]):  # Show first 3
                        with st.expander(f"{question['skill_type'].title()}: {question['prompt'][:50]}..."):
                            st.write(f"**Question:** {question['prompt']}")
                            st.write("**Options:**")
                            for j, option in enumerate(question['options']):
                                st.write(f"{j+1}. {option}")
                            st.write(f"**Explanation:** {question['explanation']}")
                else:
                    st.error("Failed to get soft skills questions")
            except Exception as e:
                st.error(f"Error: {e}")


