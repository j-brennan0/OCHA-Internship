<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Displacement Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f5f7fa;
      margin: 20px;
    }
    h1 {
      text-align: center;
    }
    .container {
      max-width: 1200px;
      margin: auto;
    }
    .card {
      background: white;
      padding: 20px;
      margin-bottom: 20px;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    table {
      width: 100%;
      border-collapse: collapse;
    }
    th, td {
      padding: 10px;
      border-bottom: 1px solid #ddd;
      text-align: left;
    }
    th {
      background: #2c3e50;
      color: white;
    }
  </style>
</head>
<body>

<div class="container">
  <h1>Displacement by City Dashboard</h1>

  <!-- Chart -->
  <div class="card">
    <canvas id="displacementChart"></canvas>
  </div>

  <!-- Table -->
  <div class="card">
    <h3>Displacement Summary</h3>
    <table>
      <thead>
        <tr>
          <th>City / Location</th>
          <th>County</th>
          <th>Total Displaced Individuals</th>
        </tr>
      </thead>
      <tbody id="tableBody"></tbody>
    </table>
  </div>
</div>

<script>
  // ✅ Replace this with real aggregated data from your dataset
  const data = [
    { city: "Abyei Youth Center", county: "Abyei", total: 10300 },
    { city: "Mangalla Site", county: "Juba", total: 6053 },
    { city: "Rokon Center", county: "Juba", total: 2335 },
    { city: "Ayod Centre", county: "Ayod", total: 700 },
    { city: "Kanal/Canal", county: "Ayod", total: 6155 }
  ];

  // Populate table
  const tableBody = document.getElementById("tableBody");
  data.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.city}</td>
      <td>${row.county}</td>
      <td>${row.total.toLocaleString()}</td>
    `;
    tableBody.appendChild(tr);
  });

  // Chart
  const ctx = document.getElementById('displacementChart').getContext('2d');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.map(d => d.city),
      datasets: [{
        label: 'Displaced Individuals',
        data: data.map(d => d.total),
        backgroundColor: '#3498db'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
</script>

</body>
</html>
