
async function callOp(endpoint) {
  const a = document.getElementById('a').value;
  const b = document.getElementById('b').value;
  const resEl = document.getElementById('result');
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

document.getElementById('btn-add').addEventListener('click', () => callOp('add'));
document.getElementById('btn-subtract').addEventListener('click', () => callOp('subtract'));
document.getElementById('btn-multiply').addEventListener('click', () => callOp('multiply'));
document.getElementById('btn-divide').addEventListener('click', () => callOp('divide'));
