
async function callOp(endpoint) {
  const a = document.getElementById('a').value;
  const b = document.getElementById('b').value;
  const resEl = document.getElementById('result');
  // show immediate feedback so users know something happened
  if (resEl) resEl.textContent = 'Calculating...';
  try {
    const res = await fetch('/' + endpoint, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({a: Number(a), b: Number(b)})
    });
    const data = await res.json();
    if (res.ok) {
      resEl.textContent = 'Result: ' + data.result;
    } else {
      resEl.textContent = 'Error: ' + (data.detail || 'Unknown error');
    }
    console.log(endpoint, data);
  } catch (e) {
    resEl.textContent = 'Error: ' + e.message;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const bind = (id, endpoint) => {
    const el = document.getElementById(id);
    if (!el) {
      console.warn(`Element #${id} not found, skipping binding for ${endpoint}`);
      return;
    }
    el.addEventListener('click', () => {
      console.debug(`clicked ${id} -> calling ${endpoint}`);
      callOp(endpoint);
    });
  };

  bind('btn-add', 'add');
  bind('btn-subtract', 'subtract');
  bind('btn-multiply', 'multiply');
  bind('btn-divide', 'divide');
  bind('btn-power', 'power');
});
