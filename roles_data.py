"""
roles_data.py
--------------
Defines the roles this portal can match a resume against, and the skill
vocabulary used to detect skills inside resume text.

To add a new role: add an entry to ROLES with a "skills" list (drawn from,
or extending, SKILL_VOCABULARY) and a one-line "description".
"""

# Master list of recognizable skills/keywords across roles.
# Extend this as you add more roles or want finer-grained matching.
SKILL_VOCABULARY = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "sql", "nosql",
    "react", "angular", "vue", "node.js", "express", "django", "flask", "spring",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "git", "ci/cd", "jenkins", "linux", "bash", "rest api", "graphql", "microservices",
    "machine learning", "deep learning", "data analysis", "data visualization",
    "pandas", "numpy", "tensorflow", "pytorch", "scikit-learn", "statistics",
    "excel", "power bi", "tableau", "sql server", "etl", "data pipelines",
    "agile", "scrum", "jira", "confluence", "project management", "roadmapping",
    "stakeholder management", "product strategy", "user research", "a/b testing",
    "communication", "leadership", "problem solving", "customer support",
    "ticketing systems", "zendesk", "salesforce", "crm", "customer success",
    "onboarding", "account management", "html", "css", "sass", "figma",
    "ui design", "ux design", "responsive design", "accessibility",
    "mongodb", "mysql", "postgresql", "redis", "unit testing", "test automation",
    "selenium", "manual testing", "bug tracking", "api testing", "load testing",
    "network administration", "windows server", "active directory", "vmware",
    "monitoring", "incident management", "sla management", "escalation handling",
]

# Skills that are behavioral/interpersonal rather than tool-based — used to
# split a role's missing skills into "skill development" vs "personal
# development" recommendations.
SOFT_SKILLS = {
    "communication", "leadership", "problem solving", "stakeholder management",
    "user research", "project management", "account management", "customer success",
    "onboarding", "escalation handling", "sla management", "incident management",
    "agile", "scrum", "a/b testing", "roadmapping", "product strategy",
    "customer support",
}

# Concrete, hands-on suggestions for closing a technical/tool skill gap.
# Skills not listed here fall back to a generic template.
SKILL_TIPS = {
    "sql": "Practice writing queries against a real dataset — joins, aggregations, and window functions come up constantly in interviews.",
    "python": "Build one small end-to-end script or automation (e.g. a report generator) — a working project speaks louder than a bullet point.",
    "git": "Get comfortable with branches, merges, and pull requests — most teams expect this as table stakes, not a taught skill.",
    "docker": "Containerize one of your own projects, even a simple one, so you can speak to it concretely in interviews.",
    "kubernetes": "Start with a managed cluster (e.g. a free-tier GKE/EKS trial) and deploy a small containerized app to see the concepts in action.",
    "aws": "Work through AWS's free-tier tutorials for the services relevant to this role (EC2, S3, Lambda) rather than just reading about them.",
    "azure": "Use Azure's free-tier sandbox to complete one hands-on module relevant to this role.",
    "gcp": "Use Google Cloud's free-tier credits to complete one hands-on project.",
    "rest api": "Build or consume a small REST API, even a toy project, so you can talk through request/response design confidently.",
    "linux": "Spend time in a Linux terminal daily — navigating, permissions, process management — until it's second nature.",
    "bash": "Automate one repetitive task you already do manually with a short shell script.",
    "excel": "Practice pivot tables, VLOOKUP/XLOOKUP, and core formulas on a real dataset until they're fast, not fiddly.",
    "tableau": "Build one dashboard from a public dataset end-to-end so you have a concrete example ready to discuss.",
    "power bi": "Build one report from a public dataset so you have a real example to walk through.",
    "selenium": "Automate a test for a simple public website to get hands-on with locators and waits.",
    "jira": "Use Jira, or a free equivalent, to track a personal project — boards, sprints, and issue types.",
    "figma": "Recreate an interface you like in Figma to build fluency with components and layout.",
    "zendesk": "If you don't have access to Zendesk, walk through its documentation and trial account to learn the ticket workflow.",
}

# Suggestions for building a soft/behavioral skill through everyday practice.
DEV_TIPS = {
    "communication": "Look for chances to present or write summaries for non-technical stakeholders — it's the fastest way to build this skill visibly.",
    "leadership": "Volunteer to lead a small project or mentor a colleague, even informally, and note the outcome on your resume.",
    "problem solving": "Keep a short log of tricky problems you've solved and how — concrete examples matter more than the label itself.",
    "stakeholder management": "Practice by managing communication for a cross-team task, even a small one, and document how you kept people aligned.",
    "user research": "Run a handful of informal user interviews or feedback sessions on any project you're involved in.",
    "project management": "Take ownership of planning and tracking one project end-to-end, however small.",
    "account management": "Take on ownership of a client or internal relationship, even informally, and track the outcomes.",
    "customer success": "Look for chances to follow up with customers after their issue is resolved, to build a habit of proactive care.",
    "onboarding": "Volunteer to help onboard a new teammate or customer and document the process you used.",
    "escalation handling": "Ask to shadow or take on escalated tickets to build direct experience handling high-stakes issues.",
    "sla management": "Track your own response/resolution times against a target for a few weeks to build the habit.",
    "incident management": "Volunteer for on-call or incident-response rotations if available, even in a supporting role.",
    "agile": "Join or observe a few sprint ceremonies — standups, retros, planning — to get comfortable with the rhythm.",
    "scrum": "Look for exposure to a Scrum team's ceremonies, or a short certification if it's genuinely useful for the role.",
    "a/b testing": "Run a small experiment, even on a side project, to get hands-on with hypothesis framing and reading results.",
    "roadmapping": "Practice by sketching a rough roadmap for a project you're close to, even informally.",
    "product strategy": "Practice articulating the 'why' behind a product decision you've observed or been part of.",
    "customer support": "Take on a few support tickets or customer questions directly, even outside your usual role, to build direct experience.",
}

ROLES = {
    "Technical Support Engineer": {
        "description": "Front-line troubleshooting, ticket resolution, and customer-facing technical help.",
        "skills": [
            "customer support", "ticketing systems", "zendesk", "sql", "linux",
            "bash", "rest api", "communication", "problem solving",
            "incident management", "escalation handling", "jira",
        ],
    },
    "Backend Developer": {
        "description": "Building and maintaining server-side logic, APIs, and databases.",
        "skills": [
            "python", "java", "node.js", "sql", "nosql", "rest api", "graphql",
            "microservices", "docker", "git", "postgresql", "mongodb", "redis",
            "unit testing",
        ],
    },
    "Frontend Developer": {
        "description": "Building user-facing interfaces and interactive web experiences.",
        "skills": [
            "javascript", "typescript", "react", "angular", "vue", "html", "css",
            "sass", "responsive design", "accessibility", "figma", "git",
        ],
    },
    "DevOps Engineer": {
        "description": "Automating infrastructure, deployment pipelines, and system reliability.",
        "skills": [
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
            "ci/cd", "jenkins", "linux", "bash", "monitoring", "git",
        ],
    },
    "Data Analyst": {
        "description": "Turning raw data into reports and insights that drive decisions.",
        "skills": [
            "sql", "excel", "power bi", "tableau", "python", "pandas", "numpy",
            "statistics", "data visualization", "etl", "data pipelines",
        ],
    },
    "QA Engineer": {
        "description": "Ensuring software quality through manual and automated testing.",
        "skills": [
            "manual testing", "test automation", "selenium", "api testing",
            "load testing", "bug tracking", "jira", "sql", "git",
        ],
    },
    "Product Manager": {
        "description": "Defining product direction and coordinating teams to ship it.",
        "skills": [
            "product strategy", "roadmapping", "stakeholder management",
            "user research", "a/b testing", "agile", "scrum", "jira",
            "communication", "leadership",
        ],
    },
    "Customer Success Manager": {
        "description": "Driving retention and growth through strong customer relationships.",
        "skills": [
            "customer success", "account management", "onboarding", "crm",
            "salesforce", "communication", "stakeholder management",
            "problem solving",
        ],
    },
    "System Administrator": {
        "description": "Maintaining servers, networks, and IT infrastructure.",
        "skills": [
            "linux", "windows server", "active directory", "network administration",
            "vmware", "bash", "monitoring", "incident management", "sla management",
        ],
    },
    "Machine Learning Engineer": {
        "description": "Building and deploying models that learn from data.",
        "skills": [
            "python", "machine learning", "deep learning", "tensorflow", "pytorch",
            "scikit-learn", "pandas", "numpy", "statistics", "sql", "docker",
        ],
    },
}
