# Role Finder Portal

A local web app: upload a resume and get back

- an **ATS compatibility score** (0-100) with plain-language fixes,
- a **ranked match** against ten roles (Technical Support Engineer, Backend
  Developer, Data Analyst, DevOps Engineer, and more), and
- if you pick a **target role**, a tailored action plan split into skills to
  develop, personal/behavioral development, and specific resume edits.

## Files

- `app.py` — Flask server (routes: the page, and `/analyze` for uploads)
- `resume_matcher.py` — text extraction, ATS scoring, and role/plan matching logic
- `roles_data.py` — roles, skill vocabulary, and the tips used in the target-role plan
- `templates/index.html`, `static/style.css`, `static/script.js` — the web page
- `requirements.txt` — dependencies (Flask, pdfplumber, python-docx)

## Setup in VS Code

1. Open this folder in VS Code (`File > Open Folder...`).
2. Open a terminal: `` Ctrl+` ``
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   ```
   Windows: `venv\Scripts\activate`
   macOS/Linux: `source venv/bin/activate`

   > If PowerShell blocks activation with an "execution policy" error, run:
   > `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
   > then type `Y` to confirm, and try activating again.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running it

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser. Optionally pick a
target role from the dropdown, then drop in a resume (PDF, DOCX, or TXT).
If you change the target role afterward, it automatically re-runs the plan
against the same resume — no need to re-upload.

Stop the server with `Ctrl+C` in the terminal when you're done.

## How the ATS score works

The 100-point score is built from checks that are actually measurable from
resume text: contact info present (15 pts), standard section headers like
Experience/Education/Skills (18 pts), resume length (12 pts), bullet-point
usage (15 pts), general keyword variety (15 pts), and how well your skills
match the target role's keywords, or the best-matching role if none is
chosen (25 pts). Each deduction comes with a plain-language fix in the
results.

## Customizing roles and advice

Open `roles_data.py`:
- `SKILL_VOCABULARY` — the full list of skills the app can detect in a resume.
- `ROLES` — each role's description and required skills (drawn from `SKILL_VOCABULARY`).
- `SOFT_SKILLS` — which of those skills count as behavioral/interpersonal
  (routed to "Personal Development") vs. technical (routed to "Skills to Develop").
- `SKILL_TIPS` / `DEV_TIPS` — the specific advice shown for each skill gap;
  skills without an entry fall back to a generic template.

To add a role, add an entry to `ROLES`. To detect a new skill, add it to
`SKILL_VOCABULARY` first, then reference it in whichever roles need it, and
optionally add a tip for it in `SKILL_TIPS` or `DEV_TIPS`.

## Notes

- Matching is keyword-based (skills mentioned in the resume text), not a full
  semantic read of experience — treat results as a starting point.
- Uploaded files are processed in a temporary location and deleted immediately
  after analysis; nothing is stored.
