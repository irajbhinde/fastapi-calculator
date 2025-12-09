// app/static/calculations.js

function getToken() {
  return window.localStorage.getItem("access_token");
}

function authHeaders() {
  const token = getToken();
  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

document.addEventListener("DOMContentLoaded", () => {
  const createForm = document.getElementById("create-calc-form");
  const editForm = document.getElementById("edit-calc-form");
  const tableBody = document.getElementById("calc-table-body");
  const reloadBtn = document.getElementById("reload-calcs-btn");

  const errorEl = document.getElementById("calc-error");
  const successEl = document.getElementById("calc-success");
  const detailsEl = document.getElementById("calc-details");
  const editHelper = document.getElementById("edit-helper-text");

  if (!createForm || !tableBody) {
    console.warn("BREAD elements not found on this page.");
    return;
  }

  // If user is not logged in (no JWT), show message and disable forms.
  if (!getToken()) {
    errorEl.textContent =
      "You are not logged in. Please log in first to manage calculations.";
    createForm.querySelectorAll("input, select, button").forEach((el) => {
      el.disabled = true;
    });
    editForm.querySelectorAll("input, select, button").forEach((el) => {
      el.disabled = true;
    });
    return;
  }

  function setError(msg) {
    errorEl.textContent = msg || "";
  }

  function setSuccess(msg) {
    successEl.textContent = msg || "";
  }

  function clearMessages() {
    setError("");
    setSuccess("");
  }

  async function loadCalculations() {
    clearMessages();
    detailsEl.textContent = "";
    editHelper.textContent = "Select a calculation above and click \"Edit\".";

    try {
      const resp = await fetch("/calculations", {
        method: "GET",
        headers: authHeaders(),
      });

      if (!resp.ok) {
        setError("Failed to load calculations.");
        tableBody.innerHTML = "";
        return;
      }

      const data = await resp.json();
      tableBody.innerHTML = "";

      if (!Array.isArray(data) || data.length === 0) {
        tableBody.innerHTML =
          '<tr><td colspan="8" style="text-align:center;">No calculations yet.</td></tr>';
        return;
      }

      for (const calc of data) {
        const tr = document.createElement("tr");
        tr.dataset.id = calc.id;
        tr.dataset.a = calc.a;
        tr.dataset.b = calc.b;
        tr.dataset.type = calc.type;
        tr.dataset.note = calc.note || "";
        tr.dataset.result = calc.result;

        tr.innerHTML = `
          <td>${calc.id}</td>
          <td>${calc.a}</td>
          <td>${calc.b}</td>
          <td>${calc.type}</td>
          <td>${calc.result ?? ""}</td>
          <td>${calc.note ?? ""}</td>
          <td>${calc.created_at ?? ""}</td>
          <td>
            <button type="button" class="view-btn">View</button>
            <button type="button" class="edit-btn">Edit</button>
            <button type="button" class="delete-btn">Delete</button>
          </td>
        `;
        tableBody.appendChild(tr);
      }
    } catch (err) {
      console.error(err);
      setError("Network error while loading calculations.");
    }
  }

  // CREATE / ADD
  createForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearMessages();

    const aInput = document.getElementById("calc-a");
    const bInput = document.getElementById("calc-b");
    const typeSelect = document.getElementById("calc-type");
    const noteInput = document.getElementById("calc-note");

    const a = parseFloat(aInput.value);
    const b = parseFloat(bInput.value);
    const type = typeSelect.value;
    const note = noteInput.value.trim() || null;

    if (Number.isNaN(a) || Number.isNaN(b)) {
      setError("Please enter valid numeric values for A and B.");
      return;
    }

    if (!type) {
      setError("Please choose an operation type.");
      return;
    }

    try {
      const resp = await fetch("/calculations", {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify({ a, b, type, note }),
      });

      if (!resp.ok) {
        const data = await resp.json().catch(() => ({}));
        setError(
          data.detail || "Failed to create calculation. Please try again."
        );
        return;
      }

      const data = await resp.json();
      setSuccess("Calculation created successfully.");
      // reset note only so user can quickly add more
      noteInput.value = "";
      await loadCalculations();
      await fetchCalculationStats();  
    } catch (err) {
      console.error(err);
      setError("Network error while creating calculation.");
    }
  });

  // BROWSE / READ / EDIT / DELETE (via event delegation)
  tableBody.addEventListener("click", async (e) => {
    const target = e.target;
    if (!(target instanceof HTMLElement)) return;

    const tr = target.closest("tr");
    if (!tr || !tr.dataset.id) return;

    const id = tr.dataset.id;

    if (target.classList.contains("view-btn")) {
      // READ
      detailsEl.textContent = `Calculation #${id}: ${tr.dataset.a} ${tr.dataset.type} ${tr.dataset.b} = ${tr.dataset.result}. Note: ${tr.dataset.note || "(none)"}`;
      setSuccess("");
      setError("");
      return;
    }

    if (target.classList.contains("edit-btn")) {
      // Fill edit form
      document.getElementById("edit-calc-id").value = id;
      document.getElementById("edit-a").value = tr.dataset.a || "";
      document.getElementById("edit-b").value = tr.dataset.b || "";
      document.getElementById("edit-type").value = tr.dataset.type || "";
      document.getElementById("edit-note").value = tr.dataset.note || "";
      editHelper.textContent = `Editing calculation #${id}`;
      setSuccess("");
      setError("");
      return;
    }

    if (target.classList.contains("delete-btn")) {
      if (!confirm(`Delete calculation #${id}?`)) return;

      try {
        const resp = await fetch(`/calculations/${id}`, {
          method: "DELETE",
          headers: authHeaders(),
        });

        if (!resp.ok) {
          const data = await resp.json().catch(() => ({}));
          setError(
            data.detail || "Failed to delete calculation. Please try again."
          );
          return;
        }

        setSuccess(`Calculation #${id} deleted successfully.`);
        await loadCalculations();
        await fetchCalculationStats();  
      } catch (err) {
        console.error(err);
        setError("Network error while deleting calculation.");
      }
    }
  });

  // EDIT / UPDATE
  editForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearMessages();

    const id = document.getElementById("edit-calc-id").value;
    if (!id) {
      setError("No calculation selected to edit.");
      return;
    }

    const aRaw = document.getElementById("edit-a").value;
    const bRaw = document.getElementById("edit-b").value;
    const type = document.getElementById("edit-type").value;
    const noteRaw = document.getElementById("edit-note").value;

    const payload = {};

    if (aRaw !== "") {
      const a = parseFloat(aRaw);
      if (Number.isNaN(a)) {
        setError("Edit A must be a valid number.");
        return;
      }
      payload["a"] = a;
    }

    if (bRaw !== "") {
      const b = parseFloat(bRaw);
      if (Number.isNaN(b)) {
        setError("Edit B must be a valid number.");
        return;
      }
      payload["b"] = b;
    }

    if (type) {
      payload["type"] = type;
    }

    if (noteRaw !== "") {
      payload["note"] = noteRaw.trim();
    }

    if (Object.keys(payload).length === 0) {
      setError("Please change at least one field before saving.");
      return;
    }

    try {
      const resp = await fetch(`/calculations/${id}`, {
        method: "PUT",
        headers: authHeaders(),
        body: JSON.stringify(payload),
      });

      if (!resp.ok) {
        const data = await resp.json().catch(() => ({}));
        setError(
          data.detail || "Failed to update calculation. Please try again."
        );
        return;
      }

      await resp.json();
      setSuccess(`Calculation #${id} updated successfully.`);
      await loadCalculations();
      await fetchCalculationStats(); 
    } catch (err) {
      console.error(err);
      setError("Network error while updating calculation.");
    }
  });

  // Reload button
  reloadBtn.addEventListener("click", async () => {
    await loadCalculations();
  });

  // Initial load
  loadCalculations();
});


// --- Usage stats / report ---

async function fetchCalculationStats() {
  try {
    const resp = await fetch("/api/calculations/stats");
    if (!resp.ok) {
      throw new Error("Failed to load stats");
    }
    const data = await resp.json();
    renderCalculationStats(data);
  } catch (err) {
    console.error("Error fetching stats", err);
    const el = document.getElementById("calc-error");
    if (el) {
      el.textContent = "Failed to load stats.";
    }
  }
}

function renderCalculationStats(stats) {
  const setText = (id, value) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent =
      value === null || value === undefined ? "–" : String(value);
  };

  setText("stat-total-calcs", stats.total_calculations);
  setText("stat-add-count", stats.add_count);
  setText("stat-subtract-count", stats.subtract_count);
  setText("stat-multiply-count", stats.multiply_count);
  setText("stat-divide-count", stats.divide_count);
  setText("stat-power-count", stats.power_count);
  setText("stat-avg-a", stats.average_a?.toFixed?.(2) ?? stats.average_a);
  setText("stat-avg-b", stats.average_b?.toFixed?.(2) ?? stats.average_b);
  setText(
    "stat-avg-result",
    stats.average_result?.toFixed?.(2) ?? stats.average_result
  );
}

// Make sure stats load on page load
document.addEventListener("DOMContentLoaded", () => {
  fetchCalculationStats();
});
