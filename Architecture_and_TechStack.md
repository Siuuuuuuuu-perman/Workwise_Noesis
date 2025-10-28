Architecture and Tech Stack — WorkWise Noesis

High-Level Architecture
User → Frontend (React or Streamlit) → FastAPI Backend → MCP Orchestrator → NIM (Nemotron + agents) → External APIs (O*NET, Courses, Jobs) → DB

Components
- Frontend: React (Vite + Tailwind) or Streamlit for fastest demo; chat UI + tables + charts.
- Backend: FastAPI with async routes; task orchestration; caching; feature flags.
- Agents (MCP):
  - Skill Agent: normalize/extract skills from text (Nemotron via NIM)
  - Gap Agent: compare against O*NET role skills; classify Known/Partial/Missing
  - Learning Agent: query course providers; rank by relevance/rating/duration/preference
  - Job Agent: fetch/sample job postings; extract skills; compute overlap
  - Risk Agent: lightweight automation-risk heuristic with rationale
- Models via NIM: Host Nemotron for NLU; optional embeddings for similarity search.
- Data: SQLite (demo) or Postgres; seed O*NET snapshot; optional sample course/job caches.

Data Flow (MVP)
1. Upload/profile text + goal → /plan
2. Backend calls /extract (Nemotron) → skills JSON
3. Backend calls /gap → status per skill and missing list
4. Backend calls /recommend → ranked resources
5. Backend calls /roadmap → week-by-week plan
6. Backend calls /jobs and /risk → job samples and risk score
7. Persist plan; return aggregated payload for UI

APIs (Backend)
- POST /extract {text}
- POST /gap {skills, target_role}
- POST /recommend {skills_missing, prefs}
- POST /roadmap {recommendations, weekly_hours}
- GET /jobs?role=…&region=…
- GET /risk?role=…
- POST /plan {input} → returns consolidated response

Tech Stack
- Language: Python 3.11+
- Backend: FastAPI, httpx/requests, pydantic, uvicorn, asyncio
- Frontend: React + Vite + Tailwind; or Streamlit for speed
- Agents: MCP SDK (multi-agent patterns)
- Models: NVIDIA Nemotron via NIM; optional vector DB (FAISS/pgvector) for resources
- DB: SQLite (dev), PostgreSQL (prod)
- Infra: Docker; NVIDIA AI Workbench; .env for keys; GitHub Actions (optional)

Build Plan (Hackathon)
- Hour 0–0.5: Scaffold FastAPI + simple UI (file upload, goal input)
- Hour 0.5–1.0: Implement /plan calling mocked providers with sample data
- Hour 1.0–1.5: Integrate Nemotron via NIM for real extraction; refine gap logic
- Hour 1.5–2.0: Implement recommendations and roadmap; add chat; polish UI
- Stretch: persist plans; progress tracking; export PDF; basic telemetry

Security & Privacy
- Client-side redaction option for PII; HTTPS-only; token-scoped keys; delete-on-demand.

Observability
- Structured logs; latency metrics for each step; error budgets; minimal tracing.

