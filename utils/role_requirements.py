from utils.llm_engine import ask_llm


def get_role_requirements(role):

    prompt = f"""
    You are an AI hiring expert.

    For the role: {role}

    Give only the top technical skills required.

    Return only comma separated skills.

    Example:
    python, sql, machine learning, deep learning
    """

    response = ask_llm(prompt)

    skills = response.lower().split(",")

    cleaned_skills = []

    for skill in skills:

        cleaned_skills.append(skill.strip())

    return cleaned_skills