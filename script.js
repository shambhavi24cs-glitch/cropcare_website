// Update data every 10 seconds
async function updateLiveData() {
  try {
    const res  = await fetch('http://127.0.0.1:5000/latest');
    const data = await res.json();

    document.getElementById('dash-temp').textContent = data.temp;
    document.getElementById('dash-hum').textContent  = data.humidity;
    document.getElementById('dash-soil').textContent = data.soil;
  } catch (err) {
    console.error("Error fetching live data:", err);
  }
}

// Initial fetch and set interval
updateLiveData();
setInterval(updateLiveData, 10000);

// Define state for spray toggle
let mainSprayOn = false;

// When farmer clicks Spray button:
async function toggleMainSpray() {
  const endpoint = mainSprayOn ? '/spray-off' : '/spray-on';
  try {
    await fetch('http://127.0.0.1:5000' + endpoint, { method: 'POST' });
    mainSprayOn = !mainSprayOn; // toggle the state
    
    // Update UI
    const btn = document.getElementById('spray-btn');
    const btnText = btn.querySelector('.btn-text');
    
    if (mainSprayOn) {
      btn.classList.add('active');
      btnText.textContent = 'Spray System: ON';
    } else {
      btn.classList.remove('active');
      btnText.textContent = 'Spray System: OFF';
    }
  } catch (error) {
    console.error("Error toggling spray:", error);
    alert("Could not connect to the server.");
  }
}