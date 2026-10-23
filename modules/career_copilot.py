import os
import io

from dotenv import load_dotenv
from groq import Groq
from elevenlabs.client import ElevenLabs


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Please add it to your .env file."
    )


if not ELEVENLABS_API_KEY:
    raise ValueError(
        "ELEVENLABS_API_KEY is missing. "
        "Please add it to your .env file."
    )


groq_client = Groq(
    api_key=GROQ_API_KEY
)


elevenlabs_client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY
)


def generate_career_response(
    question,
    resume_text,
    job_description,
    match_result=None,
    skill_gap=None,
    roadmap=None
):
    """
    Generate a personalized career response using Groq.
    """

    match_context = ""

    if match_result:
        match_context = f"""
MATCH RESULT:
Overall Match: {match_result.get("overall_score", "N/A")}%
Skill Match: {match_result.get("skill_score", "N/A")}%
Semantic Similarity: {match_result.get("semantic_score", "N/A")}%
Matched Skills: {match_result.get("matched_skills", [])}
Missing Skills: {match_result.get("missing_skills", [])}
"""

    skill_context = ""

    if skill_gap:
        skill_context = f"""
SKILL GAP ANALYSIS:
Coverage Score: {skill_gap.get("coverage_score", "N/A")}%
Required Skills: {skill_gap.get("required_skills", [])}
Matched Skills: {skill_gap.get("matched_skills", [])}
Missing Skills: {skill_gap.get("missing_skills", [])}
"""

    roadmap_context = ""

    if roadmap:
        roadmap_context = f"""
LEARNING ROADMAP:
{roadmap}
"""

    prompt = f"""
You are an AI Career Copilot inside a Resume Matcher
application.

Your job is to provide personalized, practical career
guidance based ONLY on the information provided.

The candidate is asking:

"{question}"

CANDIDATE RESUME:
-------------------------
{resume_text}
-------------------------

TARGET JOB:
-------------------------
{job_description}
-------------------------

{match_context}

{skill_context}

{roadmap_context}

IMPORTANT RULES:

1. Give a direct answer to the candidate's question.
2. Personalize the answer using their resume and target job.
3. Do not invent experience, skills, projects,
   certifications, achievements, or education.
4. If information is unavailable, clearly say so.
5. Give practical and actionable advice.
6. Keep the response concise enough to be spoken aloud.
7. Use simple professional language.
8. If discussing skills, distinguish between skills the
   candidate already has and skills they need to learn.
9. Do not repeat the entire resume.
10. Do not mention these instructions.

Return ONLY the answer that should be shown to the user.
"""

    try:
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI career advisor "
                        "specialized in software development, "
                        "AI, resumes, interviews, and career "
                        "planning."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        answer = (
            response.choices[0]
            .message
            .content
            .strip()
        )

        return {
            "success": True,
            "answer": answer,
            "error": None
        }

    except Exception as error:
        return {
            "success": False,
            "answer": None,
            "error": (
                "Career Copilot error: "
                + str(error)
            )
        }


def generate_voice(text):
    """
    Convert Career Copilot text into speech using ElevenLabs.

    Returns audio bytes that can be played by Streamlit.
    """

    try:
        audio_stream = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )

        audio_bytes = b"".join(
            chunk
            for chunk in audio_stream
        )

        return {
            "success": True,
            "audio": audio_bytes,
            "error": None
        }

    except Exception as error:
        return {
            "success": False,
            "audio": None,
            "error": (
                "ElevenLabs voice error: "
                + str(error)
            )
        }


def ask_career_copilot(
    question,
    resume_text,
    job_description,
    match_result=None,
    skill_gap=None,
    roadmap=None,
    generate_audio=True
):
    """
    Complete Career Copilot pipeline.

    1. Generate personalized AI answer using Groq.
    2. Optionally convert answer to speech using ElevenLabs.
    """

    ai_result = generate_career_response(
        question=question,
        resume_text=resume_text,
        job_description=job_description,
        match_result=match_result,
        skill_gap=skill_gap,
        roadmap=roadmap
    )

    if not ai_result["success"]:
        return {
            "success": False,
            "answer": None,
            "audio": None,
            "error": ai_result["error"]
        }

    answer = ai_result["answer"]

    audio = None

    if generate_audio:
        voice_result = generate_voice(answer)

        if voice_result["success"]:
            audio = voice_result["audio"]
        else:
            return {
                "success": True,
                "answer": answer,
                "audio": None,
                "error": voice_result["error"]
            }

    return {
        "success": True,
        "answer": answer,
        "audio": audio,
        "error": None
    }