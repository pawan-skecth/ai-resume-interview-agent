from utils.skills_database import MASTER_SKILLS


def extract_skills(text):

    text = text.lower()

    detected_skills = []

    for skill in MASTER_SKILLS:

        if skill.lower() in text:
            detected_skills.append(skill)

    return list(set(detected_skills))