"""
resume_matcher.py
------------------
Text extraction and skill-matching logic, shared by app.py.
"""

import os
import re

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import docx  # python-docx
except ImportError:
    docx = None

from roles_data import ROLES, SKILL_VOCABULARY, SOFT_SKILLS, SKILL_TIPS, DEV_TIPS

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"(\+?\d[\d\-\s()]{8,}\d)")
BULLET_RE = re.compile(r"^\s*[-•*\u2022\u25CF\u2013]\s+")
SECTION_HEADERS = ["experience", "education", "skills", "projects", "certifications", "summary"]
CORE_SECTIONS = ["experience", "education", "skills"]


class UnsupportedFileType(Exception):
    pass


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        if pdfplumber is None:
            raise RuntimeError("pdfplumber is not installed. Run: pip install pdfplumber")
        chunks = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                chunks.append(page.extract_text() or "")
        return "\n".join(chunks)

    elif ext == ".docx":
        if docx is None:
            raise RuntimeError("python-docx is not installed. Run: pip install python-docx")
        document = docx.Document(file_path)
        return "\n".join(p.text for p in document.paragraphs)

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    else:
        raise UnsupportedFileType(f"Unsupported file type: {ext}. Use .pdf, .docx, or .txt")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def find_skills(text: str, skill_list) -> set:
    text_norm = normalize(text)
    found = set()
    for skill in skill_list:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_norm):
            found.add(skill)
    return found


def resume_health_check(text: str) -> dict:
    return {
        "has_email": bool(EMAIL_RE.search(text)),
        "has_phone": bool(PHONE_RE.search(text)),
        "word_count": len(text.split()),
        "sections_found": [s for s in SECTION_HEADERS if s in text.lower()],
    }


def match_roles(resume_text: str, top_n: int = 6) -> list:
    """Return roles ranked by match percentage against the resume's detected skills."""
    resume_skills = find_skills(resume_text, SKILL_VOCABULARY)

    results = []
    for role_name, role_info in ROLES.items():
        required = set(role_info["skills"])
        matched = resume_skills & required
        missing = required - resume_skills
        score = round(len(matched) / len(required) * 100, 1) if required else 0.0
        results.append({
            "role": role_name,
            "description": role_info["description"],
            "score": score,
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing),
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_n], sorted(resume_skills)


def compute_role_match(resume_skills: set, role_name: str) -> dict:
    """Match against a single named role, regardless of the top_n cutoff above."""
    role_info = ROLES[role_name]
    required = set(role_info["skills"])
    matched = resume_skills & required
    missing = required - resume_skills
    score = round(len(matched) / len(required) * 100, 1) if required else 0.0
    return {
        "role": role_name,
        "description": role_info["description"],
        "score": score,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
    }


def bullet_usage_ratio(text: str) -> float:
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return 0.0
    bulleted = [l for l in lines if BULLET_RE.match(l)]
    return len(bulleted) / len(lines)


def calculate_ats_score(text: str, health: dict, resume_skills: set,
                         best_role_score_frac: float) -> dict:
    """Score resume/ATS-friendliness out of 100, with a plain-language issue list.

    best_role_score_frac is a 0-1 fraction: the target role's match fraction
    if one was chosen, otherwise the top-ranked role's match fraction — this
    is the 'does this resume speak the right keywords' component.
    """
    issues = []
    breakdown = {}

    # Contact info — 15 pts
    contact_pts = 0
    if health["has_email"]:
        contact_pts += 8
    else:
        issues.append("No email address detected — add one so recruiters and ATS parsers can find you.")
    if health["has_phone"]:
        contact_pts += 7
    else:
        issues.append("No phone number detected — include one near the top of your resume.")
    breakdown["contact_info"] = contact_pts

    # Standard section headers — 18 pts
    found_core = [s for s in CORE_SECTIONS if s in health["sections_found"]]
    section_pts = len(found_core) * 6
    for s in CORE_SECTIONS:
        if s not in found_core:
            issues.append(f"Add a clearly labeled '{s.title()}' section — ATS software looks for standard headings.")
    breakdown["section_structure"] = section_pts

    # Length — 12 pts
    wc = health["word_count"]
    if 300 <= wc <= 1100:
        length_pts = 12
    elif wc < 150:
        length_pts = 0
        issues.append("Resume looks very short — ATS and recruiters may read this as incomplete. Aim for 400-800 words.")
    elif wc < 300:
        length_pts = 6
        issues.append("Resume is on the shorter side — consider adding more detail to your experience bullets.")
    else:
        length_pts = 6
        issues.append("Resume is quite long — consider trimming to the most relevant content.")
    breakdown["length"] = length_pts

    # Bullet point usage — 15 pts
    ratio = bullet_usage_ratio(text)
    if ratio >= 0.15:
        bullet_pts = 15
    elif ratio > 0:
        bullet_pts = 8
        issues.append("Use bullet points more consistently in your experience section — ATS parsers and recruiters both scan bullets faster than paragraphs.")
    else:
        bullet_pts = 0
        issues.append("No bullet points detected — switch dense paragraphs into scannable bullet points.")
    breakdown["bullet_usage"] = bullet_pts

    # General keyword variety — 15 pts
    variety_pts = round(min(len(resume_skills), 10) * 1.5, 1)
    if len(resume_skills) < 5:
        issues.append("Few recognizable skill keywords were found — list your tools and technologies explicitly, not just implied by job titles.")
    breakdown["keyword_variety"] = variety_pts

    # Role keyword match — 25 pts
    role_pts = round(best_role_score_frac * 25, 1)
    breakdown["role_keyword_match"] = role_pts

    total = round(contact_pts + section_pts + length_pts + bullet_pts + variety_pts + role_pts, 1)
    total = min(total, 100.0)

    if total >= 80:
        rating = "Excellent"
    elif total >= 60:
        rating = "Good"
    elif total >= 40:
        rating = "Needs Work"
    else:
        rating = "Poor"

    return {"score": total, "rating": rating, "breakdown": breakdown, "issues": issues}


def build_role_plan(role_name: str, resume_skills: set, ats_issues: list) -> dict:
    """A concrete action plan for one target role: skill gaps split into
    technical vs. behavioral development, plus specific resume edits."""
    match = compute_role_match(resume_skills, role_name)
    missing = match["missing_skills"]

    technical_gaps = [s for s in missing if s not in SOFT_SKILLS]
    soft_gaps = [s for s in missing if s in SOFT_SKILLS]

    skill_development = [
        {"skill": s, "tip": SKILL_TIPS.get(s, f"Get hands-on with {s} through a small project or a short course — direct experience beats reading about it.")}
        for s in technical_gaps
    ]
    personal_development = [
        {"skill": s, "tip": DEV_TIPS.get(s, f"Look for chances to practice {s} in your current role, then note the outcome on your resume.")}
        for s in soft_gaps
    ]

    resume_changes = list(ats_issues[:3])
    if missing:
        top_missing = missing[:3]
        resume_changes.append(
            f"Work these terms into your Experience or Skills section, using the exact phrasing employers use for {role_name}: "
            + ", ".join(top_missing) + "."
        )
    resume_changes.append(
        f"Quantify your impact (tickets closed, time saved, users affected) in your bullet points — "
        f"specific numbers stand out for {role_name} roles more than a list of duties."
    )

    return {
        "role": role_name,
        "description": match["description"],
        "score": match["score"],
        "matched_skills": match["matched_skills"],
        "missing_skills": missing,
        "skill_development": skill_development,
        "personal_development": personal_development,
        "resume_changes": resume_changes[:6],
    }


def suggest_focus_skills(role_matches: list, top_n: int = 5) -> list:
    """Rank missing skills by how much learning them would improve overall fit.

    A skill counts more when it's missing from several roles, and more again
    when those roles are already a moderate/strong fit (close to being real
    options) rather than a distant long shot — so the list favors the
    highest-leverage thing to learn next, not just the most common gap.
    """
    from collections import defaultdict

    impact = defaultdict(float)
    unlocks = defaultdict(set)

    for role in role_matches:
        weight = 1 + (role["score"] / 100)
        for skill in role["missing_skills"]:
            impact[skill] += weight
            unlocks[skill].add(role["role"])

    ranked = sorted(impact.items(), key=lambda item: item[1], reverse=True)[:top_n]
    return [
        {"skill": skill, "helps_with": sorted(unlocks[skill])}
        for skill, _ in ranked
    ]


def analyze_resume(file_path: str, target_role: str = None) -> dict:
    text = extract_text(file_path)
    health = resume_health_check(text)
    role_matches, detected_skills = match_roles(text)
    resume_skills = set(detected_skills)

    # The fraction that feeds the ATS "role keyword match" component:
    # the chosen target role's fit if one was given, else the best current match.
    if target_role and target_role in ROLES:
        best_frac = compute_role_match(resume_skills, target_role)["score"] / 100
    elif role_matches:
        best_frac = role_matches[0]["score"] / 100
    else:
        best_frac = 0.0

    ats = calculate_ats_score(text, health, resume_skills, best_frac)

    result = {
        "health": health,
        "detected_skills": detected_skills,
        "roles": role_matches,
        "ats": ats,
    }

    if target_role and target_role in ROLES:
        result["target_plan"] = build_role_plan(target_role, resume_skills, ats["issues"])
    else:
        result["focus_skills"] = suggest_focus_skills(role_matches)

    return result
