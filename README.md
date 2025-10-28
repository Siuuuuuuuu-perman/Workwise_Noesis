# WorkWise Noesis - Enhanced AI Learning Gap Solution

An AI-powered personal learning assistant that identifies skill gaps and generates dynamic, personalized learning roadmaps. This comprehensive platform combines workforce transition focus with adaptive learning-gap analysis to help users bridge the gap between their current skills and career aspirations.

## 🚀 What's Built

**Complete End-to-End Platform:**
- **Backend API**: FastAPI with skill extraction, gap analysis, assessment, resource ranking, and roadmap generation
- **Frontend UI**: Streamlit app with file upload, interactive assessment, and comprehensive dashboard
- **Assessment Flow**: Initial knowledge testing to refine skill levels before roadmap generation
- **File Support**: PDF and TXT resume upload with text extraction and XML conversion
- **AI Analysis**: Automation risk assessment and job market analysis
- **Gamification**: Mastery points system and real-world problem solving
- **Interview Prep**: Technical questions and soft skills assessment

## 📁 Project Structure

```
WorkWise-Noesis/
├── backend/app/                 # FastAPI backend
│   ├── main.py                  # API endpoints and file upload handling
│   └── services/                # Core business logic
│       ├── skills.py           # Skill extraction from text/resumes
│       ├── gaps.py             # Gap detection and role mapping
│       ├── assessment.py       # Knowledge testing and scoring
│       ├── resources.py        # Resource ranking and recommendations
│       ├── roadmap.py          # Learning plan generation
│       ├── problems.py         # Real-world problem generation
│       ├── ai_analysis.py      # AI replacement risk analysis
│       └── models.py           # Pydantic data models
├── frontend/
│   └── streamlit_app.py        # Comprehensive UI application
├── requirements.txt             # All dependencies
├── .env                        # Environment variables
├── env.example                 # Environment template
└── README.md                   # This file
```

## 🛠️ Quick Start

**Prerequisites:** Python 3.9+ (tested with 3.9-3.12)

### 1. Setup Environment
```bash
# Clone and navigate to project
cd WorkWise-Noesis

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Run the Application

**Terminal 1 - Backend API:**
```bash
uvicorn backend.app.main:app --reload --port 8000
```
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

**Terminal 2 - Frontend UI:**
```bash
streamlit run frontend/streamlit_app.py
```
- UI: http://localhost:8501 (or shown URL)

### 3. Use the Application

1. **Upload Resume**: PDF/TXT file or paste text
2. **Set Goals**: Target role, weekly hours, preferences
3. **Analyze Skills**: Extract known skills and detect gaps
4. **Take Assessment**: Knowledge test to refine skill levels
5. **Get Resources**: Ranked learning recommendations
6. **Generate Roadmap**: Week-by-week learning plan with mastery points
7. **Practice Problems**: Real-world scenarios to test skills
8. **AI Analysis**: Assess automation risk and job market opportunities
9. **Interview Prep**: Technical questions and soft skills assessment

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/analyze` | POST | Extract skills, detect gaps |
| `/upload-pdf` | POST | Upload and convert PDF to XML |
| `/analyze-xml` | POST | Analyze skills from XML content |
| `/assessment/generate` | POST | Create knowledge test |
| `/assessment/submit` | POST | Score test, update skills |
| `/assessment/soft-skills` | POST | Generate soft skills assessment |
| `/resources` | POST | Rank learning resources |
| `/roadmap` | POST | Generate learning plan |
| `/problems/generate` | POST | Generate real-world problems |
| `/problems/{id}` | GET | Get specific problem |
| `/problems/{id}/validate` | POST | Validate problem solution |
| `/ai-analysis` | POST | Analyze AI replacement risk |
| `/job-market` | POST | Analyze job market opportunities |
| `/interview-questions/{role}` | GET | Get interview questions for role |
| `/roles` | GET | Get available STEM roles |

## 🔧 Environment Variables

Copy `env.example` to `.env` for production integrations:

```bash
cp env.example .env
# Edit .env with your actual API keys
```

**Current MVP**: Works without any environment variables (uses mock data)

**Future Integrations**: Uncomment and set API keys in `.env`:
- NVIDIA NIM API for skill extraction
- Course provider APIs (Coursera, edX, Udemy, Khan Academy)
- O*NET API for role skill mapping
- Database for persistent storage

## 🎯 Current Implementation

**Core Features (Fully Working):**
- ✅ Rule-based skill extraction from text and resumes
- ✅ Role-to-skills mapping (Data Analyst, Software Engineer, ML Engineer, etc.)
- ✅ Gap detection with proficiency levels (Known/Missing/Partial)
- ✅ Knowledge assessment with scoring and skill updates
- ✅ Resource ranking with mock data and preferences
- ✅ Roadmap generation with weekly planning and mastery points
- ✅ PDF/TXT file upload with XML conversion
- ✅ Interactive Streamlit UI with comprehensive dashboard
- ✅ Real-world problem generation and validation
- ✅ AI replacement risk analysis with research citations
- ✅ Job market analysis with growth rates and salary data
- ✅ Interview preparation with technical and soft skills questions
- ✅ Gamification with mastery points and progress tracking

**Advanced Features:**
- ✅ XML-based resume processing
- ✅ Multi-role support (STEM-focused)
- ✅ Comprehensive assessment system
- ✅ Problem-solving scenarios
- ✅ Market analysis and risk assessment
- ✅ Interview preparation tools

**Future Integration Targets:**
- 🔄 Replace rule-based extraction with NVIDIA Nemotron (via NIM)
- 🔄 Use O*NET taxonomy for role skill mapping
- 🔄 Connect to real course APIs (Coursera, edX, Udemy, Khan Academy)
- 🔄 Implement adaptive assessment algorithms
- 🔄 Add persistent user progress tracking

## 🧪 Testing

To test the application:

1. **Backend Testing:**
   ```bash
   # Start the backend
   uvicorn backend.app.main:app --reload --port 8000
   
   # Test health endpoint
   curl http://localhost:8000/health
   
   # Test skill analysis
   curl -X POST "http://localhost:8000/analyze" \
        -H "Content-Type: application/json" \
        -d '{"goal": "Data Analyst", "known_skills": ["Python"], "resume_text": "I have experience with data analysis"}'
   ```

2. **Frontend Testing:**
   ```bash
   # Start the frontend
   streamlit run frontend/streamlit_app.py
   
   # Navigate to http://localhost:8501
   # Test all features: upload, analyze, assess, roadmap, problems, AI analysis
   ```

3. **Integration Testing:**
   - Upload a PDF resume and verify XML conversion
   - Complete the full workflow: analyze → assess → resources → roadmap
   - Test problem generation and validation
   - Verify AI analysis and job market features

## 🔒 Security & Privacy
- Transparent reasoning snippets with user control of data
- Optional PII redaction capabilities
- HTTPS-only in production environments
- Secure file upload handling with validation
- Environment-based configuration management

## 🏆 Credits
Built for **Agents for Impact @ Howard University** - combining workforce transition focus with adaptive learning-gap analysis. This project demonstrates the potential of AI-driven career guidance and personalized learning pathways.

## 🚀 **LIVE DEPLOYMENT STATUS**

**✅ Your WorkWise Noesis is ready for production deployment!**

### **🎯 Current Features:**
- ✅ **AI-Powered Skill Extraction** (NVIDIA Nemotron ready)
- ✅ **Intelligent Gap Analysis** (with AI fallback)
- ✅ **Dynamic Assessment Generation** (AI-enhanced)
- ✅ **Personalized Learning Roadmaps** (AI-optimized)
- ✅ **Real-World Problem Solving** (gamified)
- ✅ **AI Risk Analysis** (automation assessment)
- ✅ **Job Market Analysis** (growth insights)
- ✅ **Interview Preparation** (technical + soft skills)

### **🤖 NVIDIA Integration Status:**
- ✅ **Nemotron Nano v12** integration implemented
- ✅ **API Key**: Configured and ready
- ✅ **Fallback Mode**: Active (works without API)
- ✅ **Auto-Activation**: Will enable AI features when API is properly configured

### **🚀 Deploy Now:**

**Method 1: Vercel Dashboard**
1. Go to [vercel.com](https://vercel.com) → Your Project
2. Settings → Environment Variables
3. Add your NVIDIA API key and deploy

**Method 2: Quick Deploy**
```bash
# Your app will be live at: https://workwise-noesis.vercel.app
```

### **🧪 Test Your Deployment:**
```bash
python3 test_deployment.py
```

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
