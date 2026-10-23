import json
import time

from modules.ai_analyzer import client


# ============================================================
# AI PERSONALIZED LEARNING ROADMAP
# ============================================================

def generate_learning_roadmap(
    resume_text,
    job_description,
    missing_skills
):
    """
    Generate a personalized learning roadmap
    using Groq AI.
    """

    missing_skill_names = [
        item["skill"]
        if isinstance(item, dict)
        else str(item)
        for item in missing_skills
    ]

    missing_skills_text = ", ".join(
        missing_skill_names
    )

    prompt = f"""
You are an expert technical career mentor.

Create a personalized learning roadmap for a candidate
who wants to become job-ready for the target job.

Use the candidate's resume, job description, and missing
skills to create a practical roadmap.

IMPORTANT RULES:

1. Do not invent skills the candidate already has.
2. Focus primarily on missing skills.
3. Prioritize skills based on importance to the job.
4. Avoid recommending unnecessary technologies.
5. Make the roadmap realistic for a junior developer.
6. Include hands-on projects.
7. Include practical tasks.
8. Start with fundamentals and gradually move toward
   job-ready development.
9. The roadmap should cover approximately 8-12 weeks.
10. Return ONLY valid JSON.

Return exactly this structure:

{{
    "target_role": "",
    "roadmap_summary": "",
    "estimated_duration": "",
    "weeks": [
        {{
            "week": 1,
            "title": "",
            "focus": "",
            "skills": [],
            "topics": [],
            "tasks": [],
            "project": "",
            "estimated_hours": 0
        }}
    ],
    "projects": [
        {{
            "name": "",
            "description": "",
            "technologies": [],
            "difficulty": "",
            "reason": ""
        }}
    ],
    "milestones": [
        {{
            "milestone": "",
            "success_criteria": ""
        }}
    ],
    "job_readiness_checklist": []
}}

RESUME:
-------------------------
{resume_text}
-------------------------

JOB DESCRIPTION:
-------------------------
{job_description}
-------------------------

MISSING SKILLS:
-------------------------
{missing_skills_text}
-------------------------

Create a roadmap that helps the candidate close the
identified skill gaps and build projects relevant to
the target role.
"""

    max_attempts = 3

    for attempt in range(
        1,
        max_attempts + 1
    ):

        try:

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert technical "
                            "career mentor. "
                            "Always return valid JSON."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={
                    "type": "json_object"
                }
            )

            response_text = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

            try:

                roadmap = json.loads(
                    response_text
                )

                return {
                    "success": True,
                    "roadmap": roadmap,
                    "error": None
                }

            except json.JSONDecodeError:

                return {
                    "success": False,
                    "roadmap": None,
                    "error": (
                        "Groq returned invalid JSON "
                        "for the learning roadmap."
                    )
                }

        except Exception as error:

            error_message = str(error)

            temporary_error = (
                "429" in error_message
                or "rate limit"
                in error_message.lower()
                or "503" in error_message
                or "unavailable"
                in error_message.lower()
                or "timeout"
                in error_message.lower()
            )

            if temporary_error:

                if attempt < max_attempts:

                    time.sleep(
                        attempt * 3
                    )

                    continue

                return {
                    "success": False,
                    "roadmap": None,
                    "error": (
                        "Groq is temporarily busy "
                        "or the API rate limit was reached. "
                        "Please try again later."
                    )
                }

            return {
                "success": False,
                "roadmap": None,
                "error": (
                    "Roadmap generation error: "
                    + error_message
                )
            }

    return {
        "success": False,
        "roadmap": None,
        "error": (
            "Roadmap generation failed "
            "after multiple attempts."
        )
    }