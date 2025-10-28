from typing import List
from .models import RoadmapEntry, ResourceItem


def generate_learning_roadmap(
    goal: str,
    missing_skills: List[str],
    weekly_time_hours: int,
    ranked_resources: List[ResourceItem],
    weeks: int = 6,
) -> List[RoadmapEntry]:
    entries: List[RoadmapEntry] = []
    week = 1
    skill_to_resource = {r.skill.lower(): r for r in ranked_resources}
    
    # Phase 1: Foundation skills (weeks 1-2)
    foundation_skills = missing_skills[:2] if len(missing_skills) >= 2 else missing_skills
    for skill in foundation_skills:
        if week > weeks:
            break
        res = skill_to_resource.get(skill.lower())
        resource_name = res.name if res else "Self-study"
        provider = res.provider if res else ""
        entries.append(
            RoadmapEntry(
                week=week,
                topic=f"🏗️ Foundation: {skill.title()}",
                resource=f"{resource_name} ({provider})" if provider else resource_name,
                goal=f"Master basics of {skill} (50 mastery points)",
                hours=weekly_time_hours,
            )
        )
        week += 1
    
    # Phase 2: Core skills (weeks 3-4)
    core_skills = missing_skills[2:4] if len(missing_skills) > 2 else missing_skills[2:]
    for skill in core_skills:
        if week > weeks:
            break
        res = skill_to_resource.get(skill.lower())
        resource_name = res.name if res else "Self-study"
        provider = res.provider if res else ""
        entries.append(
            RoadmapEntry(
                week=week,
                topic=f"⚡ Core: {skill.title()}",
                resource=f"{resource_name} ({provider})" if provider else resource_name,
                goal=f"Build intermediate {skill} skills (75 mastery points)",
                hours=weekly_time_hours,
            )
        )
        week += 1
    
    # Phase 3: Advanced skills (weeks 5-6)
    advanced_skills = missing_skills[4:] if len(missing_skills) > 4 else []
    for skill in advanced_skills:
        if week > weeks:
            break
        res = skill_to_resource.get(skill.lower())
        resource_name = res.name if res else "Self-study"
        provider = res.provider if res else ""
        entries.append(
            RoadmapEntry(
                week=week,
                topic=f"🚀 Advanced: {skill.title()}",
                resource=f"{resource_name} ({provider})" if provider else resource_name,
                goal=f"Master advanced {skill} concepts (100 mastery points)",
                hours=weekly_time_hours,
            )
        )
        week += 1
    
    # Fill remaining weeks with projects and challenges
    while week <= weeks:
        if week == weeks:
            entries.append(
                RoadmapEntry(
                    week=week,
                    topic="🎯 Final Project",
                    resource="Real-world portfolio project",
                    goal=f"Apply all skills to solve {goal} problems (200 mastery points)",
                    hours=weekly_time_hours,
                )
            )
        else:
            entries.append(
                RoadmapEntry(
                    week=week,
                    topic="🛠️ Practice Project",
                    resource="Hands-on mini-project",
                    goal=f"Apply learned skills (50 mastery points)",
                    hours=weekly_time_hours,
                )
            )
        week += 1
    
    return entries




