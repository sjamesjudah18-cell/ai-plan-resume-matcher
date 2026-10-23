import os
import json
import time

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ============================================================
# CHECK API KEY
# ============================================================

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Please add it to your .env file."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# AI RESUME ANALYSIS
# ============================================================

def analyze_resume_with_ai(resume_text, job_description):
    """
    Analyze a resume against a job description using Groq AI.
    """

    prompt = f"""
You are an expert technical recruiter and career advisor.

Analyze the candidate's resume against the provided job description.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "candidate_profile": {{
        "name": "",
        "education": "",
        "experience": "",
        "projects": ""
    }},
    "skills": [],
    "job_fit": {{
        "summary": "",
        "fit_level": ""
    }},
    "strengths": [],
    "weaknesses": [],
    "resume_issues": [],
    "improvement_suggestions": [],
    "recommended_learning": [],
    "interview_focus": []
}}

Important rules:

1. Use only information present in the resume.
2. Never invent experience, skills, projects, education,
   achievements, or certifications.
3. Compare the resume specifically against the job description.
4. Identify important missing skills.
5. Give practical resume improvement suggestions.
6. Recommend useful technologies and topics to learn.
7. Keep recommendations suitable for a junior developer.
8. The "fit_level" must be one of:
   "Strong Fit"
   "Moderate Fit"
   "Needs Improvement"

RESUME:
-------------------------
{resume_text}
-------------------------

JOB DESCRIPTION:
-------------------------
{job_description}
-------------------------
"""

    # ========================================================
    # RETRY CONFIGURATION
    # ========================================================

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:

            # =================================================
            # SEND REQUEST TO GROQ
            # =================================================

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert technical recruiter "
                            "and career advisor. "
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

            # =================================================
            # GET RESPONSE TEXT
            # =================================================

            response_text = (
                response.choices[0]
                .message
                .content
                .strip()
            )

            # =================================================
            # PARSE JSON
            # =================================================

            try:

                analysis = json.loads(
                    response_text
                )

                return {
                    "success": True,
                    "analysis": analysis,
                    "error": None
                }

            except json.JSONDecodeError:

                return {
                    "success": False,
                    "analysis": None,
                    "error": (
                        "Groq returned an invalid JSON response."
                    )
                }

        # ====================================================
        # HANDLE API ERRORS
        # ====================================================

        except Exception as error:

            error_message = str(error)

            # ------------------------------------------------
            # TEMPORARY RATE LIMIT / SERVER ERROR
            # ------------------------------------------------

            is_temporary_error = (
                "429" in error_message
                or "rate limit" in error_message.lower()
                or "503" in error_message
                or "unavailable" in error_message.lower()
                or "timeout" in error_message.lower()
            )

            if is_temporary_error:

                if attempt < max_attempts:

                    wait_time = attempt * 3

                    time.sleep(
                        wait_time
                    )

                    continue

                return {
                    "success": False,
                    "analysis": None,
                    "error": (
                        "Groq is temporarily busy or "
                        "the API rate limit was reached. "
                        "Please wait a few seconds and try again."
                    )
                }

            # ------------------------------------------------
            # MODEL NOT FOUND
            # ------------------------------------------------

            if (
                "model_not_found" in error_message
                or "does not exist" in error_message.lower()
            ):

                return {
                    "success": False,
                    "analysis": None,
                    "error": (
                        "The selected Groq model is not "
                        "available for this API account."
                    )
                }

            # ------------------------------------------------
            # INVALID API KEY
            # ------------------------------------------------

            if (
                "401" in error_message
                or "authentication" in error_message.lower()
                or "invalid api key" in error_message.lower()
            ):

                return {
                    "success": False,
                    "analysis": None,
                    "error": (
                        "Groq API key is invalid. "
                        "Please check your .env file."
                    )
                }

            # ------------------------------------------------
            # OTHER ERRORS
            # ------------------------------------------------

            return {
                "success": False,
                "analysis": None,
                "error": (
                    "Groq AI error: "
                    + error_message
                )
            }

    # ========================================================
    # FINAL FALLBACK
    # ========================================================

    return {
        "success": False,
        "analysis": None,
        "error": (
            "AI analysis failed after multiple attempts."
        )
    }