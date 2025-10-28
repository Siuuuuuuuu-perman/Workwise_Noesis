from typing import List, Dict
from .models import SkillGap


ROLE_TO_SKILLS: Dict[str, Dict[str, Dict]] = {
    "data analyst": {
        "statistics": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Essential for hypothesis testing, A/B testing, and statistical modeling in business contexts",
            "mastery_points": 150
        },
        "python": {
            "required_proficiency": "Intermediate", 
            "required_score": 0.8,
            "reasoning": "Core tool for data manipulation, analysis, and automation. Must handle pandas, numpy, and basic ML libraries",
            "mastery_points": 200
        },
        "pandas": {
            "required_proficiency": "Advanced",
            "required_score": 0.9,
            "reasoning": "Primary library for data manipulation. Must master data cleaning, transformation, and aggregation",
            "mastery_points": 180
        },
        "sql": {
            "required_proficiency": "Advanced",
            "required_score": 0.9,
            "reasoning": "Critical for data extraction from databases. Must write complex queries and optimize performance",
            "mastery_points": 160
        },
        "data visualization": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Must create clear, actionable visualizations for stakeholders and decision makers",
            "mastery_points": 120
        },
        "tableau": {
            "required_proficiency": "Intermediate",
            "required_score": 0.6,
            "reasoning": "Industry standard for interactive dashboards and business intelligence reporting",
            "mastery_points": 140
        }
    },
    "health data analyst": {
        "statistics": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Critical for clinical research, epidemiological studies, and healthcare outcome analysis",
            "mastery_points": 200
        },
        "python": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Essential for healthcare data processing, medical imaging analysis, and predictive modeling",
            "mastery_points": 180
        },
        "sql": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Must query electronic health records, patient databases, and clinical trial data",
            "mastery_points": 160
        },
        "data visualization": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Create visualizations for clinical outcomes, patient flow analysis, and healthcare metrics",
            "mastery_points": 120
        },
        "epidemiology": {
            "required_proficiency": "Intermediate",
            "required_score": 0.6,
            "reasoning": "Understanding of disease patterns, risk factors, and population health trends",
            "mastery_points": 100
        },
        "excel": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Still widely used in healthcare for reporting, compliance, and stakeholder communication",
            "mastery_points": 80
        }
    },
    "software engineer": {
        "programming": {
            "required_proficiency": "Advanced",
            "required_score": 0.9,
            "reasoning": "Core competency for building applications, algorithms, and system design",
            "mastery_points": 250
        },
        "algorithms": {
            "required_proficiency": "Advanced", 
            "required_score": 0.8,
            "reasoning": "Essential for efficient code, system optimization, and technical interviews",
            "mastery_points": 200
        },
        "system design": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Critical for building scalable, maintainable systems and architecture decisions",
            "mastery_points": 220
        },
        "databases": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Necessary for data persistence, query optimization, and backend development",
            "mastery_points": 150
        },
        "testing": {
            "required_proficiency": "Intermediate",
            "required_score": 0.6,
            "reasoning": "Ensures code quality, reliability, and maintainability in production systems",
            "mastery_points": 120
        },
        "version control": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Essential for collaboration, code management, and deployment workflows",
            "mastery_points": 100
        }
    },
    "machine learning engineer": {
        "python": {
            "required_proficiency": "Advanced",
            "required_score": 0.9,
            "reasoning": "Primary language for ML libraries (TensorFlow, PyTorch, scikit-learn)",
            "mastery_points": 200
        },
        "statistics": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Foundation for understanding ML algorithms, model validation, and experimental design",
            "mastery_points": 180
        },
        "machine learning": {
            "required_proficiency": "Advanced",
            "required_score": 0.9,
            "reasoning": "Core competency in supervised/unsupervised learning, deep learning, and model optimization",
            "mastery_points": 250
        },
        "data preprocessing": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Critical for cleaning, transforming, and preparing data for ML models",
            "mastery_points": 180
        },
        "model deployment": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Essential for putting ML models into production and maintaining them",
            "mastery_points": 160
        },
        "cloud platforms": {
            "required_proficiency": "Intermediate",
            "required_score": 0.6,
            "reasoning": "Necessary for scalable ML infrastructure (AWS, GCP, Azure)",
            "mastery_points": 140
        }
    },
    "cybersecurity analyst": {
        "network security": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Core competency for protecting network infrastructure and detecting threats",
            "mastery_points": 200
        },
        "incident response": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Critical for rapid threat detection, containment, and recovery procedures",
            "mastery_points": 180
        },
        "penetration testing": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Essential for vulnerability assessment and security testing",
            "mastery_points": 160
        },
        "security tools": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Proficiency with SIEM, firewalls, IDS/IPS, and security monitoring tools",
            "mastery_points": 140
        },
        "compliance": {
            "required_proficiency": "Intermediate",
            "required_score": 0.6,
            "reasoning": "Understanding of regulations (GDPR, HIPAA, SOX) and security frameworks",
            "mastery_points": 120
        },
        "forensics": {
            "required_proficiency": "Intermediate",
            "required_score": 0.6,
            "reasoning": "Skills for digital evidence collection, analysis, and legal proceedings",
            "mastery_points": 150
        }
    },
    "biomedical engineer": {
        "biology": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Deep understanding of biological systems for medical device design",
            "mastery_points": 200
        },
        "medical devices": {
            "required_proficiency": "Advanced",
            "required_score": 0.9,
            "reasoning": "Core competency in designing, testing, and validating medical equipment",
            "mastery_points": 250
        },
        "regulatory affairs": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Critical for FDA approval processes and medical device compliance",
            "mastery_points": 180
        },
        "signal processing": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Essential for analyzing biological signals (ECG, EEG, imaging data)",
            "mastery_points": 160
        },
        "materials science": {
            "required_proficiency": "Intermediate",
            "required_score": 0.6,
            "reasoning": "Understanding biocompatible materials for implants and devices",
            "mastery_points": 140
        },
        "clinical trials": {
            "required_proficiency": "Intermediate",
            "required_score": 0.6,
            "reasoning": "Knowledge of study design, data collection, and statistical analysis",
            "mastery_points": 120
        }
    },
    "environmental engineer": {
        "environmental science": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Deep understanding of ecosystems, pollution, and environmental processes",
            "mastery_points": 200
        },
        "sustainability": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Core competency in green technologies, renewable energy, and carbon reduction",
            "mastery_points": 180
        },
        "regulatory compliance": {
            "required_proficiency": "Advanced",
            "required_score": 0.8,
            "reasoning": "Critical for EPA regulations, environmental permits, and compliance monitoring",
            "mastery_points": 160
        },
        "data analysis": {
            "required_proficiency": "Intermediate",
            "required_score": 0.7,
            "reasoning": "Essential for environmental monitoring, pollution modeling, and impact assessment",
            "mastery_points": 140
        },
        "project management": {
            "required_proficiency": "Intermediate",
            "required_score": 0.6,
            "reasoning": "Necessary for managing environmental remediation and sustainability projects",
            "mastery_points": 120
        },
        "gis": {
            "required_proficiency": "Intermediate",
            "required_score": 0.6,
            "reasoning": "Geographic Information Systems for environmental mapping and analysis",
            "mastery_points": 100
        }
    }
}


def map_role_to_required_skills(role: str) -> List[str]:
    key = (role or "").strip().lower()
    return list(ROLE_TO_SKILLS.get(key, ROLE_TO_SKILLS["data analyst"]).keys())


def detect_skill_gaps(known_skills: List[str], required_skills: List[str], role: str = "data analyst") -> List[SkillGap]:
    known = set([s.lower() for s in known_skills])
    gaps: List[SkillGap] = []
    role_key = role.lower().strip()
    role_skills = ROLE_TO_SKILLS.get(role_key, ROLE_TO_SKILLS["data analyst"])
    
    for skill in required_skills:
        skill_lower = skill.lower()
        skill_info = role_skills.get(skill_lower, {})
        
        # Determine current proficiency level
        if skill_lower in known:
            current_score = 0.8  # Assume good if mentioned
            proficiency_level = "Intermediate"
            status = "Known"
        else:
            current_score = 0.2  # Assume beginner level
            proficiency_level = "Beginner"
            status = "Missing"
        
        gaps.append(SkillGap(
            skill=skill,
            status=status,
            proficiency_level=proficiency_level,
            required_proficiency=skill_info.get("required_proficiency", "Intermediate"),
            current_score=current_score,
            required_score=skill_info.get("required_score", 0.7),
            reasoning=skill_info.get("reasoning", f"Essential skill for {role} role"),
            recommendation=f"Start with {skill.title()} basics on Coursera" if status == "Missing" else f"Advance your {skill.title()} skills",
            mastery_points=skill_info.get("mastery_points", 100)
        ))
    
    return gaps


