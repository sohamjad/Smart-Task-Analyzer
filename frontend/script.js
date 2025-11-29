// ==========================================
// SMART TASK ANALYZER — FULL FRONTEND SCRIPT
// ==========================================

const tasks = [];

// Generate Task ID from title
function idFromTitle(title, idx) {
  return title.slice(0, 10).replace(/\s+/g, '_') + '_' + idx;
}


// ====================================================
// 1. ADD TASK → Update Preview Immediately
// ====================================================

document.getElementById('task-form').addEventListener('submit', (e)=>{
  e.preventDefault();
  const title = document.getElementById('title').value.trim();
  const due_date = document.getElementById('due_date').value || null;
  const estimated_hours = parseFloat(document.getElementById('estimated_hours').value) || 1;
  const importance = parseInt(document.getElementById('importance').value) || 5;
  const deps = document.getElementById('dependencies').value.trim();
  const dependencies = deps ? deps.split(',').map(s=>s.trim()) : [];

  const id = idFromTitle(title, tasks.length);
  const t = {id, title, due_date, estimated_hours, importance, dependencies};

  tasks.push(t);

  document.getElementById('task-form').reset();
  renderPreview();   // ⭐ Show tasks immediately
});


// ====================================================
// PREVIEW ADDED TASKS BEFORE ANALYSIS
// ====================================================

function renderPreview() {
  const el = document.getElementById("preview");
  el.innerHTML = "";

  tasks.forEach(t => {
    const div = document.createElement("div");
    div.className = "task-card tag-low";

    div.innerHTML = `
      <div class="task-title">${t.title}</div>
      <div class="task-meta">Due: ${t.due_date || '—'} | Hours: ${t.estimated_hours} | Importance: ${t.importance}</div>
      <div class="task-explain">Dependencies: ${t.dependencies.join(', ') || "None"}</div>
    `;

    el.appendChild(div);
  });
}


// ====================================================
// 2. ANALYZE TASKS BUTTON CLICK
// ====================================================

document.getElementById('analyze').addEventListener('click', async ()=>{
  const bulkText = document.getElementById('bulk').value.trim();
  let payloadTasks = tasks.slice();

  // Bulk JSON override
  if (bulkText) {
    try {
      const parsed = JSON.parse(bulkText);
      if (Array.isArray(parsed)) payloadTasks = parsed;
      else alert("Bulk JSON must be an array");
    } catch (err) {
      alert("Invalid JSON");
      return;
    }
  }

  if (payloadTasks.length === 0) {
    alert("No tasks provided");
    return;
  }

  const strategy = document.getElementById('strategy').value;
  const btn = document.getElementById('analyze');
  btn.textContent = "Analyzing...";
  btn.disabled = true;

  try {
    // SEND TO BACKEND
    const res = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({tasks: payloadTasks, strategy})
    });

    const data = await res.json();

    // Render Sections
    renderResults(data.tasks);
    renderMatrix(data.tasks);

    // Suggestions
    const q = encodeURIComponent(JSON.stringify(payloadTasks));
    const sres = await fetch(`http://127.0.0.1:8000/api/tasks/suggest/?tasks=${q}&strategy=${strategy}`);
    const sdata = await sres.json();
    renderSuggestions(sdata.suggestions || []);

  } catch (err) {
    console.error(err);
    alert("Network error");
  }

  btn.textContent = "Analyze Tasks";
  btn.disabled = false;
});


// ====================================================
// 3. RENDER SORTED RESULTS
// ====================================================

function renderResults(list) {
  const el = document.getElementById('results');
  el.innerHTML = '';

  list.forEach(t => {
    const div = document.createElement('div');

    // Highlight circular dependencies (score=0)
    const highlightClass =
      t.score === 0 ? "tag-high" :
      t.score >= 70 ? "tag-high" :
      t.score >= 40 ? "tag-medium" : "tag-low";

    div.className = "task-card " + highlightClass;

    div.innerHTML = `
      <div class="task-title">${t.title} — <span style="font-weight:600">score: ${t.score}</span></div>
      <div class="task-meta">
        Due: ${t.due_date || '—'} | 
        Hours: ${t.estimated_hours} | 
        Importance: ${t.importance}
      </div>
      <div class="task-explain">Why: ${t.explanation}</div>
    `;
    el.appendChild(div);
  });
}


// ====================================================
// 4. RENDER SUGGESTIONS
// ====================================================

function renderSuggestions(list) {
  const el = document.getElementById('suggestions-list');
  el.innerHTML = '';

  list.forEach(s => {
    const div = document.createElement('div');
    div.className = "task-card tag-low";

    div.innerHTML = `
      <div class="task-title">${s.task.title} — score: ${s.task.score}</div>
      <div class="task-explain">Why: ${s.why}</div>
    `;

    el.appendChild(div);
  });
}



// ====================================================
// ⭐ 5. EISENHOWER MATRIX LOGIC
// ====================================================

function renderMatrix(list) {
  document.getElementById("ui").innerHTML = "";
  document.getElementById("uni").innerHTML = "";
  document.getElementById("nui").innerHTML = "";
  document.getElementById("nuni").innerHTML = "";

  list.forEach(t => {
    const dueDate = t.due_date ? new Date(t.due_date) : null;
    const today = new Date();

    // urgent = due within 2 days
    const urgent = dueDate ? ((dueDate - today) / (1000 * 3600 * 24) <= 2) : false;

    // importance threshold
    const important = t.importance >= 7;

    const item = document.createElement("div");
    item.textContent = `${t.title} (${t.score})`;

    if (urgent && important)
      document.getElementById("ui").appendChild(item);

    else if (urgent && !important)
      document.getElementById("uni").appendChild(item);

    else if (!urgent && important)
      document.getElementById("nui").appendChild(item);

    else
      document.getElementById("nuni").appendChild(item);
  });
}
