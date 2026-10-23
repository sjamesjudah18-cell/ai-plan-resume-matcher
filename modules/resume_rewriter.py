import json
import time

from modules.ai_analyzer import client


# ============================================================
# AI RESUME REWRITER
# ============================================================

def rewrite_resume_section(
    resume_section,
    job_description,
    section_type
):
    """
    Rewrite a resume section for a target job using Groq AI.

    The AI must preserve factual information and must not
    invent experience, skills, projects, achievements,
    technologies, metrics, or certifications.
    """

    prompt = f"""
You are an expert technical resume writer and ATS specialist.

Rewrite the provided resume section so that it is stronger,
clearer, more professional, and better aligned with the
target job description.

IMPORTANT FACTUAL RULES:

1. NEVER invent information.
2. NEVER add technologies the candidate did not mention.
3. NEVER invent achievements.
4. NEVER invent numbers, percentages, metrics, users,
   performance improvements, rankings, or impact.
5. NEVER invent work experience.
6. NEVER invent certifications.
7. NEVER invent projects.
8. Preserve the candidate's actual meaning.
9. You may improve wording, structure, clarity, grammar,
   and professional presentation.
10. You may naturally emphasize skills that already appear
    in the supplied section.
11. Use ATS-friendly terminology only when supported by
    the candidate's actual information.
12. If something is missing, do not fabricate it.

TARGET SECTION:
{section_type}

RESUME SECTION:
-------------------------
{resume_section}
-------------------------

TARGET JOB DESCRIPTION:
-------------------------
{job_description}
-------------------------

Return ONLY valid JSON using exactly this structure:

{{
    "rewritten_text": "",
    "improvements": [],
    "ats_keywords_used": [],
    "missing_information": [],
    "fact_check_notes": []
}}

The rewritten_text should be ready to copy directly
into a professional resume.

For bullet-based sections, use concise professional
bullet points.

For summary sections, write a concise professional
paragraph.

For skills sections, organize the existing skills
clearly without adding unsupported skills.
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
                            "resume writer. "
                            "Never invent candidate information. "
                            "Always return valid JSON."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
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

                result = json.loads(
                    response_text
                )

                return {
                    "success": True,
                    "result": result,
                    "error": None
                }

            except json.JSONDecodeError:

                return {
                    "success": False,
                    "result": None,
                    "error": (
                        "Groq returned invalid JSON "
                        "for the resume rewrite."
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
                    "result": None,
                    "error": (
                        "Groq is temporarily busy "
                        "or the API rate limit was reached. "
                        "Please try again later."
                    )
                }

            if (
                "401" in error_message
                or "authentication"
                in error_message.lower()
                or "invalid api key"
                in error_message.lower()
            ):

                return {
                    "success": False,
                    "result": None,
                    "error": (
                        "Groq API key is invalid. "
                        "Please check your .env file."
                    )
                }

            return {
                "success": False,
                "result": None,
                "error": (
                    "Resume rewriting error: "
                    + error_message
                )
            }

    return {
        "success": False,
        "result": None,
        "error": (
            "Resume rewriting failed "
            "after multiple attempts."
        )
    }