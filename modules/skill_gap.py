import re


# ============================================================
# SKILL DATABASE
# ============================================================

SKILL_CATEGORIES = {

    "Programming": [
        "python",
        "java",
        "javascript",
        "typescript",
        "c++",
        "c#",
        "go",
        "rust",
    ],

    "Frontend": [
        "html",
        "css",
        "react",
        "next.js",
        "angular",
        "vue",
        "tailwind",
    ],

    "Backend": [
        "fastapi",
        "django",
        "flask",
        "node.js",
        "express",
        "rest api",
    ],

    "Database": [
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "sqlite",
        "redis",
    ],

    "AI / ML": [
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "pandas",
        "numpy",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "generative ai",
        "llm",
    ],

    "DevOps / Cloud": [
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "ci/cd",
        "github actions",
    ],

    "Tools": [
        "git",
        "github",
        "postman",
        "linux",
    ],
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):
    """
    Normalize text for reliable skill detection.
    """

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):
    """
    Extract known technical skills from text.
    """

    text = normalize_text(text)

    found_skills = []

    for category, skills in SKILL_CATEGORIES.items():

        for skill in skills:

            if skill.lower() in text:

                found_skills.append({
                    "skill": skill,
                    "category": category
                })

    return found_skills


# ============================================================
# ANALYZE SKILL GAP
# ============================================================

def analyze_skill_gap(
    resume_text,
    job_description
):
    """
    Compare resume skills against job requirements.
    """

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    resume_skill_names = {
        item["skill"]
        for item in resume_skills
    }

    matched = []
    missing = []

    for item in job_skills:

        if item["skill"] in resume_skill_names:

            matched.append(item)

        else:

            missing.append(item)

    # Remove duplicates
    matched = list({
        item["skill"]: item
        for item in matched
    }.values())

    missing = list({
        item["skill"]: item
        for item in missing
    }.values())

    # ========================================================
    # PRIORITY ASSIGNMENT
    # ========================================================

    high_priority_categories = {
        "Programming",
        "Backend",
        "Database",
        "AI / ML"
    }

    medium_priority_categories = {
        "Frontend",
        "DevOps / Cloud"
    }

    for item in missing:

        if item["category"] in high_priority_categories:

            item["priority"] = "High"

        elif item["category"] in medium_priority_categories:

            item["priority"] = "Medium"

        else:

            item["priority"] = "Low"

    # ========================================================
    # CATEGORY SUMMARY
    # ========================================================

    category_summary = {}

    for item in missing:

        category = item["category"]

        if category not in category_summary:

            category_summary[category] = []

        category_summary[category].append(
            item["skill"]
        )

    # ========================================================
    # COVERAGE SCORE
    # ========================================================

    total_required = len(
        job_skills
    )

    if total_required == 0:

        coverage_score = 0

    else:

        coverage_score = round(
            (
                len(matched)
                /
                total_required
            )
            * 100
        )

    return {
        "coverage_score": coverage_score,
        "required_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "category_summary": category_summary,
    }