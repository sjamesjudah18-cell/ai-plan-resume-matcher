import re


def extract_job_requirements(job_description):
    """
    Extract basic requirements from a job description.
    """

    text = job_description.lower()

    # Common technical skills
    skill_database = [
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
    ]

    found_skills = []

    for skill in skill_database:
        if skill.lower() in text:
            found_skills.append(skill)

    # Try to find experience requirement
    experience = None

    patterns = [
        r"(\d+)\+?\s*years?\s*(?:of)?\s*experience",
        r"(\d+)\+?\s*years?\s*(?:of)?\s*work experience",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            experience = int(match.group(1))
            break

    return {
        "skills": found_skills,
        "experience_years": experience,
    }