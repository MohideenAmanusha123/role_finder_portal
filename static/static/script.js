const dropzoneInner = document.getElementById("dropzone-inner");
const fileInput = document.getElementById("file-input");
const fileStatus = document.getElementById("file-status");
const errorMessage = document.getElementById("error-message");
const intake = document.getElementById("intake");
const loading = document.getElementById("loading");
const results = document.getElementById("results");
const resultsFilename = document.getElementById("results-filename");
const healthPanel = document.getElementById("health-panel");
const atsPanel = document.getElementById("ats-panel");
const planPanel = document.getElementById("plan-panel");
const focusPanel = document.getElementById("focus-panel");
const focusList = document.getElementById("focus-list");
const rolesHeading = document.getElementById("roles-heading");
const roleList = document.getElementById("role-list");
const resetButton = document.getElementById("reset-button");
const targetRoleSelect = document.getElementById("target-role-select");

let currentFile = null;

dropzoneInner.addEventListener("click", () => fileInput.click());
dropzoneInner.setAttribute("tabindex", "0");
dropzoneInner.setAttribute("role", "button");
dropzoneInner.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    fileInput.click();
  }
});

["dragenter", "dragover"].forEach((evt) => {
  dropzoneInner.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzoneInner.classList.add("is-dragover");
  });
});

["dragleave", "drop"].forEach((evt) => {
  dropzoneInner.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzoneInner.classList.remove("is-dragover");
  });
});

dropzoneInner.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) handleFile(fileInput.files[0]);
});

// If the person changes their target role after results are already showing,
// re-run the analysis against the new role without asking them to re-upload.
targetRoleSelect.addEventListener("change", () => {
  if (currentFile && !results.hidden) {
    uploadFile(currentFile);
  }
});

function handleFile(file) {
  currentFile = file;
  errorMessage.hidden = true;
  fileStatus.hidden = false;
  fileStatus.textContent = `Selected: ${file.name}`;
  uploadFile(file);
}

async function uploadFile(file) {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("target_role", targetRoleSelect.value);

  intake.hidden = true;
  results.hidden = true;
  loading.hidden = false;

  try {
    const response = await fetch("/analyze", { method: "POST", body: formData });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Something went wrong.");
    }

    renderResults(data);
  } catch (err) {
    loading.hidden = true;
    intake.hidden = false;
    errorMessage.hidden = false;
    errorMessage.textContent = err.message;
  }
}

function tierFor(score) {
  if (score >= 70) return { className: "tier-strong", label: "STRONG FIT" };
  if (score >= 40) return { className: "tier-moderate", label: "MODERATE FIT" };
  return { className: "tier-low", label: "LOW FIT" };
}

function ratingColor(rating) {
  if (rating === "Excellent") return "var(--stamp)";
  if (rating === "Good") return "var(--stamp)";
  if (rating === "Needs Work") return "var(--amber)";
  return "var(--error)";
}

function ringSvg(score, radius, strokeColor) {
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - score / 100);
  const size = radius * 2 + 10;
  const center = size / 2;
  return `
    <svg viewBox="0 0 ${size} ${size}">
      <circle class="ring-track" cx="${center}" cy="${center}" r="${radius}"></circle>
      <circle class="ring-value" cx="${center}" cy="${center}" r="${radius}"
        stroke="${strokeColor}"
        stroke-dasharray="${circumference}"
        stroke-dashoffset="${circumference}"
        data-final-offset="${offset}"></circle>
    </svg>
  `;
}

function renderHealth(h) {
  healthPanel.innerHTML = `
    <div class="health__item">
      <p class="health__label">EMAIL</p>
      <p class="health__value ${h.has_email ? "is-good" : "is-bad"}">${h.has_email ? "Found" : "Not found"}</p>
    </div>
    <div class="health__item">
      <p class="health__label">PHONE</p>
      <p class="health__value ${h.has_phone ? "is-good" : "is-bad"}">${h.has_phone ? "Found" : "Not found"}</p>
    </div>
    <div class="health__item">
      <p class="health__label">WORD COUNT</p>
      <p class="health__value">${h.word_count}</p>
    </div>
    <div class="health__item">
      <p class="health__label">SECTIONS</p>
      <p class="health__value">${h.sections_found.length ? h.sections_found.join(", ") : "None detected"}</p>
    </div>
  `;
}

function renderAts(ats) {
  const color = ratingColor(ats.rating);
  const issuesHtml = ats.issues.length
    ? `<ul class="ats-panel__issues">${ats.issues.map((i) => `<li>${i}</li>`).join("")}</ul>`
    : `<p class="ats-panel__clean">No major ATS red flags detected.</p>`;

  atsPanel.innerHTML = `
    <div class="ats-panel__ring">
      ${ringSvg(ats.score, 39, color)}
      <div class="ats-panel__ring-label">
        <span class="ats-panel__ring-score">${ats.score}</span>
        <span class="ats-panel__ring-total">/ 100</span>
      </div>
    </div>
    <div class="ats-panel__body">
      <p class="ats-panel__eyebrow">ATS COMPATIBILITY · ${ats.rating.toUpperCase()}</p>
      <h3 class="ats-panel__title">How well this resume parses for applicant tracking systems</h3>
      ${issuesHtml}
    </div>
  `;
}

function renderPlanSection(title, items, emptyText) {
  if (!items.length) {
    return `
      <div class="plan-section">
        <p class="plan-section__title">${title}</p>
        <p class="plan-empty">${emptyText}</p>
      </div>
    `;
  }
  return `
    <div class="plan-section">
      <p class="plan-section__title">${title}</p>
      ${items.map((item) => `
        <div class="plan-item">
          <span class="plan-item__bullet">→</span>
          <span><span class="plan-item__skill">${item.skill}:</span> <span class="plan-item__tip">${item.tip}</span></span>
        </div>
      `).join("")}
    </div>
  `;
}

function renderResumeChanges(changes) {
  return `
    <div class="plan-section">
      <p class="plan-section__title">RESUME CHANGES TO MAKE</p>
      ${changes.map((c) => `
        <div class="plan-item">
          <span class="plan-item__bullet">→</span>
          <span class="plan-item__tip">${c}</span>
        </div>
      `).join("")}
    </div>
  `;
}

function renderTargetPlan(plan) {
  planPanel.hidden = false;
  focusPanel.hidden = true;
  rolesHeading.textContent = "Other roles worth a look";

  planPanel.innerHTML = `
    <p class="plan-panel__eyebrow">YOUR PLAN FOR</p>
    <h2 class="plan-panel__title">${plan.role}</h2>
    <p class="plan-panel__score">${plan.score}% of this role's skills matched right now</p>
    <div class="plan-panel__skills">
      ${plan.matched_skills.map((s) => `<span class="skill-tag matched">${s}</span>`).join("")}
      ${plan.missing_skills.map((s) => `<span class="skill-tag missing">${s}</span>`).join("")}
    </div>
    ${renderPlanSection("SKILLS TO DEVELOP", plan.skill_development, "No technical gaps — your skills already line up.")}
    ${renderPlanSection("PERSONAL DEVELOPMENT", plan.personal_development, "No behavioral gaps found for this role.")}
    ${renderResumeChanges(plan.resume_changes)}
  `;
}

function renderFocusSkills(focusSkills) {
  planPanel.hidden = true;
  if (focusSkills && focusSkills.length) {
    focusPanel.hidden = false;
    focusList.innerHTML = focusSkills.map((item, i) => `
      <li class="focus-item">
        <span class="focus-item__rank">${String(i + 1).padStart(2, "0")}</span>
        <div class="focus-item__body">
          <p class="focus-item__skill">${item.skill}</p>
          <p class="focus-item__helps">Helps with: ${item.helps_with.join(", ")}</p>
        </div>
      </li>
    `).join("");
  } else {
    focusPanel.hidden = true;
  }
  rolesHeading.textContent = "Where you're the strongest fit";
}

function renderRoleList(roles) {
  roleList.innerHTML = "";
  roles.forEach((role, i) => {
    const tier = tierFor(role.score);
    const li = document.createElement("li");
    li.className = `role-card ${tier.className}`;
    li.style.setProperty("--card-delay", `${i * 0.06}s`);
    li.innerHTML = `
      <div class="role-card__ring">
        ${ringSvg(role.score, 27, "currentColor")}
        <span class="role-card__ring-label">${role.score}%</span>
      </div>
      <div class="role-card__main">
        <div class="role-card__top">
          <h3 class="role-card__title">${role.role}</h3>
          <span class="role-card__tier-label">${tier.label}</span>
        </div>
        <p class="role-card__description">${role.description}</p>
        <div class="role-card__skills">
          ${role.matched_skills.map((s) => `<span class="skill-tag matched">${s}</span>`).join("")}
          ${role.missing_skills.map((s) => `<span class="skill-tag missing">${s}</span>`).join("")}
        </div>
      </div>
    `;
    roleList.appendChild(li);
  });
}

function renderResults(data) {
  loading.hidden = true;
  results.hidden = false;
  resultsFilename.textContent = data.filename;

  renderHealth(data.health);
  renderAts(data.ats);

  if (data.target_plan) {
    renderTargetPlan(data.target_plan);
  } else {
    renderFocusSkills(data.focus_skills);
  }

  renderRoleList(data.roles);

  // Animate rings after insertion so the transition actually plays
  requestAnimationFrame(() => {
    document.querySelectorAll(".ring-value").forEach((circle) => {
      circle.style.strokeDashoffset = circle.dataset.finalOffset;
    });
  });
}

resetButton.addEventListener("click", () => {
  fileInput.value = "";
  currentFile = null;
  fileStatus.hidden = true;
  results.hidden = true;
  intake.hidden = false;
});
