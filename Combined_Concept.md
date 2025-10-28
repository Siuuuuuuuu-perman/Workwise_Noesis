WorkWise Noesis

1) Vision
WorkWise Noesis is an AI-powered career and learning copilot that identifies a person’s current skills, detects gaps against desired roles, forecasts automation risk, and generates a personalized, time-bound upskilling roadmap. It combines the workforce transition focus of WorkWise AI with the adaptive learning-gap engine of Noesis.

 2) Core Outcomes
- Personalized skill-gap analysis and automation-risk insights for a target role
- Ranked learning resources and a week-by-week roadmap aligned to the user’s availability
- Live job-market alignment (titles, skills, demand) and role recommendations
- Continuous adaptation as the user reports progress or updates goals

3) Users and Value
- Displaced or at-risk workers: actionable reskilling plans toward resilient roles
- Students and early-career professionals: clarity on skills needed to reach target jobs
- Workforce programs and universities: scalable guidance with consistent outcomes

4) Key Capabilities
- Skill extraction from resumes/LinkedIn/text (Nemotron LLM via NIM)
- Multi-agent orchestration (MCP): Skill Agent, Gap Agent, Learning Agent, Job Agent, Risk Agent
- Resource ranking from Coursera/edX/Udemy/Khan APIs and O*NET skill taxonomy mapping
- Dashboard with gap tables, roadmap timeline, progress tracking, and chat guidance

5) Data and Signals
- Inputs: resume/profile text, goals, weekly time, platform preference, region
- External data: O*NET occupations/skills, course catalogs, job listings, industry trend feeds
- Outputs: gap table, recommended resources with rationale, roadmap, job matches, risk score

6) Example Flow
User input → Nemotron (skill extraction) → MCP Agents (gap + jobs + risk + learning) → NIM inference → FastAPI backend → Frontend dashboard (tables, charts, chat)

7) Hackathon Scope (2–4 hours)
- MVP: resume/goal upload, gap table, 4–6 week roadmap, example job matches, chatbot Q&A
- Stretch: simple progress tracking, save/share plan, basic automation-risk score

8) Ethical Guardrails
- Transparent reasoning snippets, user control of data, bias checks on recommendations
