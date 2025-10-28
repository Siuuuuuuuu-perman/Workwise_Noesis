Software Requirements Specification (SRS) — WorkWise Noesis

1. Introduction
1.1 Purpose: Specify functional and non-functional requirements for an AI system that produces skill-gap analyses, automation-risk insights, and personalized learning roadmaps aligned to job roles.
1.2 Scope: MVP for hackathon: upload/profile input → analysis → dashboard with gaps, roadmap, job matches, and chat guidance.
1.3 Definitions: O*NET (occupation taxonomy), NIM (NVIDIA Inference Microservices), MCP (multi-agent orchestration), Nemotron (LLM), Roadmap (time-bound learning plan).
1.4 References: O*NET, Coursera/edX/Udemy/Khan APIs, LinkedIn/Indeed job APIs.

2. Overall Description
2.1 Product Perspective: Web app with Python FastAPI backend, LLM via NIM, agents via MCP, React/Streamlit frontend.
2.2 Product Functions:
- Extract skills and experience from text/resume.
- Map desired role to O*NET skills; compute gaps.
- Recommend and rank learning resources; generate 4–8 week roadmap.
- Retrieve example job matches and compute basic automation-risk score.
- Present results in dashboard and support Q&A via chat.
2.3 User Classes: End users (workers/students), Program admins, Demo judges.
2.4 Operating Environment: Cloud-hosted app; NVIDIA NIM endpoints; SQLite/Postgres.
2.5 Design and Implementation Constraints: 2–4 hour hackathon build; limited API keys; sample data fallbacks.
2.6 Assumptions and Dependencies: Availability of Nemotron via NIM; O*NET data snapshot; course/job APIs or cached samples.

3. System Features and Requirements
3.1 Skill Extraction
- Inputs: resume text, profile text, known skills list.
- Process: Nemotron NLU to extract entities (skills, titles, years).
- Outputs: normalized skills with confidence scores.
3.2 Gap Analysis
- Inputs: extracted skills, target role.
- Process: compare against O*NET skill list; categorize as Known/Partial/Missing.
- Outputs: gap table JSON; top missing skills.
3.3 Learning Recommendations
- Inputs: missing/partial skills; preferences (free/paid, hours/week).
- Process: fetch from course APIs or cache; rank via relevance/rating/duration/preference.
- Outputs: ranked list with title, link, duration, difficulty.
3.4 Roadmap Generation
- Inputs: ranked recommendations, weekly hours.
- Process: allocate topics over weeks; ensure coverage of gaps; add mini-projects.
- Outputs: 4–8 week plan with weekly goals and estimated hours.
3.5 Job Alignment
- Inputs: target role, region.
- Process: fetch or sample job postings; extract common skills; map back to gaps.
- Outputs: sample postings, skill overlap score.
3.6 Automation-Risk Score (Basic)
- Inputs: role, tasks (from O*NET-like data).
- Process: heuristic or lightweight model; expose rationale.
- Outputs: score 0–100 with explanation.
3.7 Dashboard & Chat
- Views: gap table, roadmap timeline, job matches, risk card.
- Chat: answer “why this course?”, “how to adjust hours?”, “alternate role?”

4. External Interface Requirements
4.1 UI: Responsive web UI; file upload; editable goal and weekly hours; save/share plan.
4.2 API Interfaces: REST JSON; endpoints: /extract, /gap, /recommend, /roadmap, /jobs, /risk, /plan.
4.3 Data: JSON payloads; SQLite/Postgres schema for users, plans, progress snapshots.

5. Non-Functional Requirements
- Performance: P95 < 2.5s per major step via NIM caching and async IO.
- Reliability: graceful degradation to cached data; retries for external APIs.
- Security: do not store resumes without consent; redact PII; HTTPS.
- Privacy: explain purpose of data use; user-controlled deletion.
- Usability: clear tables, progress meters, and tooltips; accessible color contrast.
- Maintainability: modular agents; typed Python; logging and feature flags.

6. Data Models (MVP)
- User: id, email (optional), preferences, created_at
- Plan: id, user_id, target_role, weekly_hours, created_at
- Skill: id, name, category
- PlanSkill: plan_id, skill_id, status (known/partial/missing)
- Resource: id, title, provider, url, duration_hours, difficulty, tags
- PlanWeek: plan_id, week_num, topic, goal, estimated_hours

7. Constraints and Risks
- API key limits; latency from external providers; model availability.
- Ethical risk of biased recommendations; mitigate with transparency and user review.

8. Acceptance Criteria (MVP)
- Given a resume and goal, system returns: gap table, 4–6 week roadmap, ≥3 resources, ≥3 job samples, and a risk score with rationale in < 30s end-to-end.
- UI permits editing weekly hours and regenerating roadmap without errors.


