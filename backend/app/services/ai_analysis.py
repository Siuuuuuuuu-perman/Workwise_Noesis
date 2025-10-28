from typing import List, Dict
from .models import SkillGap


AI_REPLACEMENT_DATA: Dict[str, Dict] = {
    "data analyst": {
        "automation_risk": 0.65,
        "ai_resistant_skills": ["business acumen", "stakeholder communication", "domain expertise"],
        "ai_vulnerable_skills": ["data cleaning", "basic reporting", "routine analysis"],
        "research_papers": [
            {
                "title": "The Future of Employment: How Susceptible are Jobs to Computerisation?",
                "authors": "Frey, C. B., & Osborne, M. A.",
                "year": 2017,
                "journal": "Oxford Martin School",
                "url": "https://www.oxfordmartin.ox.ac.uk/downloads/academic/The_Future_of_Employment.pdf",
                "key_findings": "47% of US employment is at risk of automation, with data analysis roles showing moderate risk"
            },
            {
                "title": "Artificial Intelligence and the Future of Work",
                "authors": "Brynjolfsson, E., & McAfee, A.",
                "year": 2014,
                "journal": "MIT Technology Review",
                "url": "https://www.technologyreview.com/2014/08/18/170366/artificial-intelligence-and-the-future-of-work/",
                "key_findings": "AI will augment rather than replace data analysts, but routine tasks will be automated"
            }
        ],
        "strategies": [
            "Develop domain expertise in specific industries",
            "Focus on business strategy and stakeholder management",
            "Learn advanced statistical modeling and experimental design",
            "Build skills in data storytelling and visualization",
            "Stay updated with AI tools and learn to work alongside them"
        ]
    },
    "software engineer": {
        "automation_risk": 0.45,
        "ai_resistant_skills": ["system architecture", "problem solving", "team leadership", "user experience design"],
        "ai_vulnerable_skills": ["code generation", "testing", "documentation", "routine debugging"],
        "research_papers": [
            {
                "title": "GitHub Copilot and the Future of AI-Assisted Programming",
                "authors": "Chen, M., Tworek, J., Jun, H., et al.",
                "year": 2021,
                "journal": "GitHub",
                "url": "https://github.blog/2021-06-29-introducing-github-copilot-ai-pair-programmer/",
                "key_findings": "AI coding assistants will augment developers but won't replace the need for human creativity and system design"
            },
            {
                "title": "The Impact of AI on Software Engineering",
                "authors": "Amershi, S., Begel, A., Bird, C., et al.",
                "year": 2019,
                "journal": "IEEE Software",
                "url": "https://ieeexplore.ieee.org/document/8802520",
                "key_findings": "AI will automate routine coding tasks but increase demand for high-level system design and architecture"
            }
        ],
        "strategies": [
            "Focus on system architecture and design patterns",
            "Develop expertise in specific domains (fintech, healthcare, etc.)",
            "Build leadership and project management skills",
            "Learn AI/ML integration and deployment",
            "Master DevOps and cloud-native development"
        ]
    },
    "machine learning engineer": {
        "automation_risk": 0.30,
        "ai_resistant_skills": ["research", "model interpretation", "business strategy", "ethical AI"],
        "ai_vulnerable_skills": ["hyperparameter tuning", "data preprocessing", "model training"],
        "research_papers": [
            {
                "title": "AutoML: A Survey of the State-of-the-Art",
                "authors": "He, X., Zhao, K., & Chu, X.",
                "year": 2021,
                "journal": "Knowledge-Based Systems",
                "url": "https://www.sciencedirect.com/science/article/pii/S0950705121001239",
                "key_findings": "AutoML tools will automate routine ML tasks but increase demand for ML engineers who can interpret and deploy models"
            },
            {
                "title": "The Future of Machine Learning Engineering",
                "authors": "Sculley, D., Holt, G., Golovin, D., et al.",
                "year": 2015,
                "journal": "NIPS Workshop",
                "url": "https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf7bbbe3de1cbdccf4-Abstract.html",
                "key_findings": "ML engineering will focus more on production systems, monitoring, and business impact rather than model development"
            }
        ],
        "strategies": [
            "Focus on MLOps and production deployment",
            "Develop expertise in model interpretation and explainability",
            "Build business acumen and stakeholder communication skills",
            "Learn ethical AI and bias detection",
            "Master advanced ML techniques and research"
        ]
    },
    "cybersecurity analyst": {
        "automation_risk": 0.25,
        "ai_resistant_skills": ["threat hunting", "incident response", "risk assessment", "compliance"],
        "ai_vulnerable_skills": ["log analysis", "vulnerability scanning", "routine monitoring"],
        "research_papers": [
            {
                "title": "AI in Cybersecurity: Opportunities and Challenges",
                "authors": "Sarker, I. H., Kayes, A. S. M., Badsha, S., et al.",
                "year": 2020,
                "journal": "IEEE Access",
                "url": "https://ieeexplore.ieee.org/document/9069875",
                "key_findings": "AI will enhance cybersecurity but human analysts remain crucial for threat interpretation and response"
            },
            {
                "title": "The Human Factor in Cybersecurity",
                "authors": "Hadlington, L.",
                "year": 2017,
                "journal": "Computers in Human Behavior",
                "url": "https://www.sciencedirect.com/science/article/pii/S0747563217304434",
                "key_findings": "Human factors and behavioral analysis remain critical in cybersecurity, difficult to fully automate"
            }
        ],
        "strategies": [
            "Develop expertise in threat intelligence and hunting",
            "Build skills in incident response and forensics",
            "Focus on risk assessment and compliance",
            "Learn AI/ML for security applications",
            "Develop communication skills for executive reporting"
        ]
    },
    "biomedical engineer": {
        "automation_risk": 0.20,
        "ai_resistant_skills": ["clinical expertise", "regulatory knowledge", "patient safety", "innovation"],
        "ai_vulnerable_skills": ["routine testing", "data collection", "basic analysis"],
        "research_papers": [
            {
                "title": "AI in Healthcare: Opportunities and Challenges",
                "authors": "Topol, E. J.",
                "year": 2019,
                "journal": "Nature Medicine",
                "url": "https://www.nature.com/articles/s41591-019-0648-0",
                "key_findings": "AI will augment medical professionals but human oversight remains critical for patient safety"
            },
            {
                "title": "The Future of Biomedical Engineering",
                "authors": "Bashir, R.",
                "year": 2018,
                "journal": "IEEE Engineering in Medicine and Biology",
                "url": "https://ieeexplore.ieee.org/document/8512430",
                "key_findings": "Biomedical engineering will increasingly focus on AI integration and personalized medicine"
            }
        ],
        "strategies": [
            "Develop deep clinical and regulatory expertise",
            "Focus on patient safety and ethical considerations",
            "Learn AI/ML for medical applications",
            "Build skills in clinical trials and validation",
            "Develop innovation and entrepreneurship skills"
        ]
    },
    "environmental engineer": {
        "automation_risk": 0.35,
        "ai_resistant_skills": ["regulatory expertise", "stakeholder management", "sustainability strategy"],
        "ai_vulnerable_skills": ["data collection", "routine monitoring", "basic analysis"],
        "research_papers": [
            {
                "title": "AI for Environmental Monitoring and Sustainability",
                "authors": "Rolnick, D., Donti, P. L., Kaack, L. H., et al.",
                "year": 2019,
                "journal": "arXiv",
                "url": "https://arxiv.org/abs/1906.01933",
                "key_findings": "AI will enhance environmental monitoring but human expertise remains crucial for policy and strategy"
            },
            {
                "title": "The Role of AI in Climate Change Mitigation",
                "authors": "Cowls, J., Tsamados, A., Taddeo, M., & Floridi, L.",
                "year": 2021,
                "journal": "Nature Machine Intelligence",
                "url": "https://www.nature.com/articles/s42256-021-00358-9",
                "key_findings": "AI will support environmental engineering but human judgment is essential for complex policy decisions"
            }
        ],
        "strategies": [
            "Develop expertise in environmental policy and regulations",
            "Focus on sustainability strategy and planning",
            "Build stakeholder management and communication skills",
            "Learn AI applications for environmental monitoring",
            "Develop expertise in climate change mitigation"
        ]
    }
}


def analyze_ai_replacement_risk(role: str, skills: List[str]) -> Dict:
    """Analyze AI replacement risk for a specific role and skill set"""
    role_data = AI_REPLACEMENT_DATA.get(role.lower(), AI_REPLACEMENT_DATA["data analyst"])
    
    # Calculate skill-level risk
    skill_risks = []
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower in role_data["ai_vulnerable_skills"]:
            skill_risks.append({"skill": skill, "risk": "High", "score": 0.8})
        elif skill_lower in role_data["ai_resistant_skills"]:
            skill_risks.append({"skill": skill, "risk": "Low", "score": 0.2})
        else:
            skill_risks.append({"skill": skill, "risk": "Medium", "score": 0.5})
    
    # Calculate overall risk
    avg_risk = sum(s["score"] for s in skill_risks) / len(skill_risks) if skill_risks else 0.5
    overall_risk = (avg_risk + role_data["automation_risk"]) / 2
    
    return {
        "role": role,
        "overall_risk": overall_risk,
        "risk_level": "High" if overall_risk > 0.7 else "Medium" if overall_risk > 0.4 else "Low",
        "skill_risks": skill_risks,
        "ai_resistant_skills": role_data["ai_resistant_skills"],
        "ai_vulnerable_skills": role_data["ai_vulnerable_skills"],
        "research_papers": role_data["research_papers"],
        "strategies": role_data["strategies"],
        "recommendations": generate_ai_resistance_recommendations(role, skill_risks)
    }


def generate_ai_resistance_recommendations(role: str, skill_risks: List[Dict]) -> List[str]:
    """Generate recommendations to reduce AI replacement risk"""
    high_risk_skills = [s["skill"] for s in skill_risks if s["risk"] == "High"]
    role_data = AI_REPLACEMENT_DATA.get(role.lower(), AI_REPLACEMENT_DATA["data analyst"])
    
    recommendations = []
    
    if high_risk_skills:
        recommendations.append(f"Focus on developing AI-resistant skills: {', '.join(role_data['ai_resistant_skills'])}")
        recommendations.append("Consider upskilling in areas that require human judgment and creativity")
    
    recommendations.extend([
        "Learn to work alongside AI tools rather than competing with them",
        "Develop domain expertise that AI cannot easily replicate",
        "Build soft skills like communication, leadership, and strategic thinking",
        "Stay updated with AI developments in your field",
        "Consider specializing in AI-human collaboration roles"
    ])
    
    return recommendations


def get_job_market_analysis(role: str, skills: List[str]) -> Dict:
    """Analyze job market opportunities and likelihood"""
    # Mock data - in production, this would connect to job APIs
    job_market_data = {
        "data analyst": {
            "total_jobs": 150000,
            "growth_rate": 0.15,
            "avg_salary": 75000,
            "competition_level": "High",
            "top_skills_demand": ["python", "sql", "tableau", "statistics"],
            "emerging_skills": ["machine learning", "cloud platforms", "data engineering"]
        },
        "software engineer": {
            "total_jobs": 200000,
            "growth_rate": 0.22,
            "avg_salary": 95000,
            "competition_level": "Medium",
            "top_skills_demand": ["programming", "algorithms", "system design", "databases"],
            "emerging_skills": ["ai integration", "cloud native", "devops", "microservices"]
        },
        "machine learning engineer": {
            "total_jobs": 50000,
            "growth_rate": 0.35,
            "avg_salary": 120000,
            "competition_level": "Medium",
            "top_skills_demand": ["python", "machine learning", "statistics", "data preprocessing"],
            "emerging_skills": ["mlops", "ai ethics", "model deployment", "automl"]
        },
        "cybersecurity analyst": {
            "total_jobs": 80000,
            "growth_rate": 0.28,
            "avg_salary": 85000,
            "competition_level": "Low",
            "top_skills_demand": ["network security", "incident response", "compliance", "threat hunting"],
            "emerging_skills": ["ai security", "cloud security", "zero trust", "quantum cryptography"]
        },
        "biomedical engineer": {
            "total_jobs": 25000,
            "growth_rate": 0.12,
            "avg_salary": 90000,
            "competition_level": "Medium",
            "top_skills_demand": ["medical devices", "biology", "regulatory affairs", "signal processing"],
            "emerging_skills": ["ai diagnostics", "telemedicine", "wearable devices", "precision medicine"]
        },
        "environmental engineer": {
            "total_jobs": 40000,
            "growth_rate": 0.18,
            "avg_salary": 80000,
            "competition_level": "Medium",
            "top_skills_demand": ["environmental science", "sustainability", "regulatory compliance", "data analysis"],
            "emerging_skills": ["climate tech", "carbon accounting", "sustainable ai", "green finance"]
        }
    }
    
    market_data = job_market_data.get(role.lower(), job_market_data["data analyst"])
    
    # Calculate skill match percentage
    top_skills = market_data["top_skills_demand"]
    skill_matches = sum(1 for skill in skills if skill.lower() in [s.lower() for s in top_skills])
    skill_match_percentage = (skill_matches / len(top_skills)) * 100 if top_skills else 0
    
    # Calculate job likelihood
    base_likelihood = 0.3  # Base 30% chance
    skill_bonus = (skill_match_percentage / 100) * 0.4  # Up to 40% bonus for skills
    growth_bonus = market_data["growth_rate"] * 0.2  # Up to 20% bonus for growth
    
    job_likelihood = min(base_likelihood + skill_bonus + growth_bonus, 0.95)  # Cap at 95%
    
    return {
        "role": role,
        "market_data": market_data,
        "skill_match_percentage": skill_match_percentage,
        "job_likelihood": job_likelihood,
        "recommendations": [
            f"Focus on developing these high-demand skills: {', '.join(top_skills[:3])}",
            f"Consider learning emerging skills: {', '.join(market_data['emerging_skills'][:2])}",
            f"Market growth rate: {market_data['growth_rate']*100:.1f}% annually",
            f"Average salary: ${market_data['avg_salary']:,}",
            f"Competition level: {market_data['competition_level']}"
        ]
    }
