from utils.llm_engine import ask_llm


def generate_interview_questions(
    role,
    topics,
    technical_count,
    difficulty
):

    prompt = f"""
You are an expert technical interviewer.

Generate interview questions using the following rules carefully.

====================================================

JOB ROLE:
{role}

TOPICS:
{topics}

DIFFICULTY:
{difficulty}

TECHNICAL QUESTION COUNT PER TOPIC:
{technical_count}

====================================================

IMPORTANT RULES:

1. Generate technical questions TOPIC WISE.

Example:
If topics are:
Python, SQL

and technical count is:
20

Then generate:
- 20 Python technical questions
- 20 SQL technical questions

2. Generate coding questions TOPIC WISE.

Generate:
- 10 coding questions per topic

If topics are:
Python, SQL

Then generate:
- 10 Python coding questions
- 10 SQL coding questions

3. Coding and Technical questions must follow the selected difficulty:
- Easy
- Medium
- Hard

4. Generate ROLE BASED sections separately.

Generate:
- 10 Role-Based Technical Questions
- 10 Domain Knowledge Questions
- 10 Scenario-Based Questions
- 10 Project-Based Questions
- 10 HR Questions

5. Role-based sections should depend ONLY on the job role,
NOT on the topics.

6. Do NOT provide answers.

7. Clearly separate every section with headings.

====================================================

OUTPUT FORMAT:

# Topic-Based Technical Questions

## Python Technical Questions
1.
2.

## SQL Technical Questions
1.
2.

# Topic-Based Coding Questions

## Python Coding Questions
1.
2.

## SQL Coding Questions
1.
2.

# Role-Based Technical Questions

1.
2.

# Domain Knowledge Questions

1.
2.

# Scenario-Based Questions

1.
2.

# Project-Based Questions

1.
2.

# HR Questions

1.
2.
"""

    response = ask_llm(prompt)

    return response