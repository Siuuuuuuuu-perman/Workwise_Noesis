# WorkWise Noesis - Enhanced AI Learning Gap Solution

An AI-powered personal learning assistant that identifies skill gaps and generates dynamic, personalized learning roadmaps. This MVP includes a complete FastAPI backend and Streamlit frontend with assessment-based skill refinement.

## 🚀 What's Built (MVP)

**Complete End-to-End Platform:**
- **Backend API**: FastAPI with skill extraction, gap analysis, assessment, resource ranking, and roadmap generation
- **Frontend UI**: Streamlit app with file upload, interactive assessment, and dashboard
- **Assessment Flow**: Initial knowledge testing to refine skill levels before roadmap generation
- **File Support**: PDF and TXT resume upload with text extraction

## 📁 Project Structure

```
WorkWise-Noesis/
├── backend/app/                 # FastAPI backend
│   ├── main.py                  # API endpoints
│   └── services/                # Core business logic
│       ├── skills.py           # Skill extraction
│       ├── gaps.py             # Gap detection
│       ├── assessment.py       # Knowledge testing
│       ├── resources.py        # Resource ranking
│       └── roadmap.py          # Learning plan generation
├── frontend/
│   └── streamlit_app.py        # UI application
├── requirements.txt             # Dependencies
├── .env                        # Environment variables
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
6. **Generate Roadmap**: Week-by-week learning plan

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/analyze` | POST | Extract skills, detect gaps |
| `/assessment/generate` | POST | Create knowledge test |
| `/assessment/submit` | POST | Score test, update skills |
| `/resources` | POST | Rank learning resources |
| `/roadmap` | POST | Generate learning plan |

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

**MVP Features (Working Now):**
- ✅ Rule-based skill extraction from text
- ✅ Role-to-skills mapping (Data Analyst, Health Data Analyst)
- ✅ Gap detection (Known/Missing/Partial)
- ✅ Knowledge assessment with scoring
- ✅ Resource ranking with mock data
- ✅ Roadmap generation with weekly planning
- ✅ File upload (PDF/TXT) with text extraction
- ✅ Interactive Streamlit UI

**Integration Targets (Future):**
- 🔄 Replace rule-based extraction with NVIDIA Nemotron (via NIM)
- 🔄 Use O*NET taxonomy for role skill mapping
- 🔄 Connect to real course APIs (Coursera, edX, Udemy, Khan Academy)
- 🔄 Implement adaptive assessment algorithms
- 🔄 Add job market analysis and automation risk scoring

## Ethics & privacy
- Transparent reasoning snippets, user control of data, optional redaction, HTTPS-only in production.

## Credits
Combines ideas from WorkWise AI and Noesis drafts; built for Agents for Impact @ Howard University.
