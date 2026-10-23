import re


# ============================================================
# COMMON ATS / JOB KEYWORDS
# ============================================================

COMMON_KEYWORDS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "react",
    "next.js",
    "node.js",
    "fastapi",
    "django",
    "flask",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "html",
    "css",
    "tailwind",
    "rest api",
    "api",
    "generative ai",
    "llm",
    "linux",
    "postman",
    "kubernetes",
    "agile",
    "scrum",
    "communication",
    "leadership",
    "problem solving",
    "teamwork",
]


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):
    """
    Normalize text for ATS-style analysis.
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
# EXTRACT KEYWORDS
# ============================================================

def extract_keywords(text):
    """
    Extract known technical and professional keywords.
    """

    text = normalize_text(text)

    found_keywords = []

    for keyword in COMMON_KEYWORDS:

        if keyword.lower() in text:

            found_keywords.append(
                keyword
            )

    return found_keywords


# ============================================================
# EXTRACT JOB KEYWORDS
# ============================================================

def extract_job_keywords(job_description):
    """
    Extract keywords specifically found in the job description.
    """

    return extract_keywords(
        job_description
    )


# ============================================================
# KEYWORD MATCHING
# ============================================================

def calculate_keyword_match(
    resume_text,
    job_description
):
    """
    Compare job-description keywords
    against the resume.
    """

    resume = normalize_text(
        resume_text
    )

    job_keywords = extract_job_keywords(
        job_description
    )

    matched_keywords = []
    missing_keywords = []

    for keyword in job_keywords:

        if keyword.lower() in resume:

            matched_keywords.append(
                keyword
            )

        else:

            missing_keywords.append(
                keyword
            )

    total_keywords = len(
        job_keywords
    )

    if total_keywords == 0:

        score = 0

    else:

        score = round(
            (
                len(matched_keywords)
                /
                total_keywords
            )
            * 100
        )

    return {
        "score": score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "total_keywords": total_keywords,
    }


# ============================================================
# RESUME STRUCTURE CHECK
# ============================================================

def check_resume_structure(resume_text):
    """
    Perform basic ATS-friendly resume structure checks.

    This is a heuristic analysis and cannot guarantee
    compatibility with every ATS.
    """

    text = normalize_text(
        resume_text
    )

    checks = []
    warnings = []
    score = 100

    # --------------------------------------------------------
    # EMPTY RESUME
    # --------------------------------------------------------

    if not text:

        return {
            "score": 0,
            "checks": [],
            "warnings": [
                "Resume text could not be extracted."
            ]
        }

    # --------------------------------------------------------
    # LENGTH
    # --------------------------------------------------------

    word_count = len(
        text.split()
    )

    if word_count < 150:

        warnings.append(
            "Resume appears very short. "
            "Consider adding relevant experience, "
            "projects, education, or skills."
        )

        score -= 15

    elif word_count > 1200:

        warnings.append(
            "Resume appears very long. "
            "Consider removing information that "
            "is not relevant to the target role."
        )

        score -= 10

    else:

        checks.append(
            "Resume length appears reasonable."
        )

    # --------------------------------------------------------
    # CONTACT INFORMATION
    # --------------------------------------------------------

    email_pattern = (
        r"[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\."
        r"[A-Za-z]{2,}"
    )

    phone_pattern = (
        r"(?:\+?\d[\d\s().-]{7,}\d)"
    )

    has_email = re.search(
        email_pattern,
        resume_text
    )

    has_phone = re.search(
        phone_pattern,
        resume_text
    )

    if has_email:

        checks.append(
            "Email address detected."
        )

    else:

        warnings.append(
            "No email address was detected."
        )

        score -= 10

    if has_phone:

        checks.append(
            "Phone number detected."
        )

    else:

        warnings.append(
            "No phone number was detected."
        )

        score -= 5

    # --------------------------------------------------------
    # COMMON SECTIONS
    # --------------------------------------------------------

    section_patterns = {
        "Education": [
            "education",
            "academic background"
        ],
        "Experience": [
            "experience",
            "work experience",
            "employment"
        ],
        "Skills": [
            "skills",
            "technical skills",
            "technologies"
        ],
        "Projects": [
            "projects",
            "personal projects",
            "academic projects"
        ],
    }

    detected_sections = []

    for section, patterns in section_patterns.items():

        found = False

        for pattern in patterns:

            if pattern in text:

                found = True
                break

        if found:

            detected_sections.append(
                section
            )

            checks.append(
                f"{section} section detected."
            )

        else:

            warnings.append(
                f"{section} section was not clearly detected."
            )

            score -= 5

    # --------------------------------------------------------
    # ATS-DANGEROUS SYMBOLS / CONTENT
    # --------------------------------------------------------

    table_like_patterns = [
        "│",
        "┃",
        "┆",
        "┊",
        "╪",
        "╫",
        "╬",
    ]

    found_table_symbols = any(
        symbol in resume_text
        for symbol in table_like_patterns
    )

    if found_table_symbols:

        warnings.append(
            "Table-like formatting symbols were detected. "
            "Complex tables can sometimes cause parsing issues "
            "in ATS systems."
        )

        score -= 5

    # --------------------------------------------------------
    # URL
    # --------------------------------------------------------

    if (
        "linkedin.com" in text
        or "github.com" in text
        or "http://" in text
        or "https://" in text
    ):

        checks.append(
            "Professional online profile/link detected."
        )

    # --------------------------------------------------------
    # BULLET POINTS
    # --------------------------------------------------------

    bullet_patterns = [
        "•",
        "- ",
        "– ",
        "* ",
    ]

    has_bullets = any(
        bullet in resume_text
        for bullet in bullet_patterns
    )

    if has_bullets:

        checks.append(
            "Bullet-style content detected."
        )

    else:

        warnings.append(
            "Few or no standard bullet points were detected. "
            "Use concise bullets for experience and projects."
        )

        score -= 5

    # --------------------------------------------------------
    # SCORE LIMIT
    # --------------------------------------------------------

    score = max(
        0,
        min(
            100,
            score
        )
    )

    return {
        "score": score,
        "checks": checks,
        "warnings": warnings,
        "detected_sections": detected_sections,
        "word_count": word_count,
    }


# ============================================================
# JOB ALIGNMENT
# ============================================================

def calculate_job_alignment(
    resume_text,
    job_description
):
    """
    Estimate how well the resume's detected keywords
    align with the target job.
    """

    keyword_result = calculate_keyword_match(
        resume_text,
        job_description
    )

    return keyword_result["score"]


# ============================================================
# ATS IMPROVEMENT SUGGESTIONS
# ============================================================

def generate_ats_suggestions(
    keyword_result,
    structure_result
):
    """
    Generate practical ATS improvement suggestions.
    """

    suggestions = []

    missing_keywords = keyword_result.get(
        "missing_keywords",
        []
    )

    # --------------------------------------------------------
    # KEYWORDS
    # --------------------------------------------------------

    if missing_keywords:

        top_missing = missing_keywords[:10]

        suggestions.append(
            "If these skills are genuinely part of your "
            "experience, consider explicitly mentioning them "
            "in your resume: "
            + ", ".join(
                skill.title()
                for skill in top_missing
            )
            + "."
        )

    # --------------------------------------------------------
    # LENGTH
    # --------------------------------------------------------

    word_count = structure_result.get(
        "word_count",
        0
    )

    if word_count < 150:

        suggestions.append(
            "Add relevant project achievements, "
            "technical skills, education, or experience."
        )

    elif word_count > 1200:

        suggestions.append(
            "Reduce unrelated or repetitive content "
            "and prioritize information relevant to the job."
        )

    # --------------------------------------------------------
    # SECTIONS
    # --------------------------------------------------------

    detected_sections = structure_result.get(
        "detected_sections",
        []
    )

    if "Skills" not in detected_sections:

        suggestions.append(
            "Add a clearly labelled Skills or "
            "Technical Skills section."
        )

    if "Projects" not in detected_sections:

        suggestions.append(
            "Add a clearly labelled Projects section "
            "if you have relevant projects."
        )

    if "Education" not in detected_sections:

        suggestions.append(
            "Add a clearly labelled Education section."
        )

    # --------------------------------------------------------
    # WARNINGS
    # --------------------------------------------------------

    warnings = structure_result.get(
        "warnings",
        []
    )

    for warning in warnings:

        if warning not in suggestions:

            suggestions.append(
                warning
            )

    return suggestions


# ============================================================
# ATS ANALYSIS
# ============================================================

def analyze_ats(
    resume_text,
    job_description
):
    """
    Perform complete ATS-style resume analysis.
    """

    keyword_result = calculate_keyword_match(
        resume_text,
        job_description
    )

    structure_result = check_resume_structure(
        resume_text
    )

    job_alignment = calculate_job_alignment(
        resume_text,
        job_description
    )

    # --------------------------------------------------------
    # WEIGHTED ATS SCORE
    # --------------------------------------------------------
    #
    # Keyword Match      = 50%
    # Structure          = 25%
    # Job Alignment      = 25%
    #
    # Job alignment currently overlaps with keyword coverage,
    # but keeping it separate makes the architecture easier
    # to improve later with AI.
    # --------------------------------------------------------

    keyword_score = keyword_result[
        "score"
    ]

    structure_score = structure_result[
        "score"
    ]

    alignment_score = job_alignment

    ats_score = round(
        (
            keyword_score * 0.50
        )
        +
        (
            structure_score * 0.25
        )
        +
        (
            alignment_score * 0.25
        )
    )

    suggestions = generate_ats_suggestions(
        keyword_result,
        structure_result
    )

    return {
        "ats_score": ats_score,
        "keyword_score": keyword_score,
        "structure_score": structure_score,
        "job_alignment_score": alignment_score,
        "matched_keywords": keyword_result[
            "matched_keywords"
        ],
        "missing_keywords": keyword_result[
            "missing_keywords"
        ],
        "total_keywords": keyword_result[
            "total_keywords"
        ],
        "structure_checks": structure_result[
            "checks"
        ],
        "structure_warnings": structure_result[
            "warnings"
        ],
        "detected_sections": structure_result.get(
            "detected_sections",
            []
        ),
        "word_count": structure_result.get(
            "word_count",
            0
        ),
        "suggestions": suggestions,
    }