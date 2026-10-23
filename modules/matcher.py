import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize text for comparison.
    """

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# EXACT SKILL MATCHING
# ============================================================

def calculate_skill_match(
    resume_text,
    required_skills
):
    """
    Compare required job skills against the resume.
    """

    resume = normalize_text(
        resume_text
    )

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        skill_normalized = skill.lower()

        if skill_normalized in resume:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )

    total_skills = len(
        required_skills
    )

    if total_skills == 0:

        score = 0

    else:

        score = round(
            (
                len(matched_skills)
                /
                total_skills
            )
            * 100
        )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


# ============================================================
# SEMANTIC SIMILARITY
# ============================================================

def calculate_semantic_similarity(
    resume_text,
    job_description
):
    """
    Calculate semantic similarity between
    the resume and job description using TF-IDF.
    """

    resume = normalize_text(
        resume_text
    )

    job = normalize_text(
        job_description
    )

    if not resume or not job:

        return 0

    documents = [
        resume,
        job
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:

        vectors = vectorizer.fit_transform(
            documents
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(
            similarity * 100
        )

    except ValueError:

        return 0


# ============================================================
# COMBINED MATCH SCORE
# ============================================================

def calculate_overall_match(
    resume_text,
    job_description,
    required_skills
):
    """
    Calculate the overall resume-job match.

    Current weighting:

    60% -> Skill Match
    40% -> Semantic Similarity
    """

    skill_result = calculate_skill_match(
        resume_text,
        required_skills
    )

    semantic_score = calculate_semantic_similarity(
        resume_text,
        job_description
    )

    skill_score = skill_result["score"]

    overall_score = round(
        (
            skill_score * 0.60
        )
        +
        (
            semantic_score * 0.40
        )
    )

    return {
        "overall_score": overall_score,
        "skill_score": skill_score,
        "semantic_score": semantic_score,
        "matched_skills": skill_result[
            "matched_skills"
        ],
        "missing_skills": skill_result[
            "missing_skills"
        ],
    }