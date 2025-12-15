document.getElementById('check').addEventListener('click', async () => {
  const out = document.getElementById('out');
  out.textContent = 'Checking...';
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab.url;
    const res = await fetch('http://localhost:3000/api/flags', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await res.json();
    out.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    out.textContent = 'Error: ' + err;
  }
});
