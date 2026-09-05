---
permalink: /ram-prices/
title: "DDR5 RAM Price Tracker (Datart)"
---

This page displays the latest DDR5 RAM prices from Datart.cz.

<!-- Chart.js setup -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<div style="width: 100%; margin: 20px 0;">
  <canvas id="chartDatart"></canvas>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const historyData = {{ site.data.ram_history | jsonify }};
  
  if (!historyData || historyData.length === 0) {
    document.querySelector('div[style*="margin"]').innerHTML = '<p>No history data available yet to render graphs.</p>';
    return;
  }

  const labels = historyData.map(entry => entry.date);
  const datasets = [
    {
      label: '8GB Min (CZK)',
      data: historyData.map(entry => entry['8GB_datart'] ?? entry['8GB_min'] ?? null),
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.1)',
      borderWidth: 2,
      pointRadius: 2,
      pointHoverRadius: 6,
      spanGaps: true,
      tension: 0.1,
      fill: false
    },
    {
      label: '8GB Avg (CZK)',
      data: historyData.map(entry => entry['8GB_avg'] ?? null),
      borderColor: 'rgb(255, 99, 132)',
      borderDash: [5, 5],
      borderWidth: 1.5,
      pointRadius: 1,
      pointHoverRadius: 5,
      spanGaps: true,
      tension: 0.1,
      fill: false
    },
    {
      label: '16GB Min (CZK)',
      data: historyData.map(entry => entry['16GB_datart'] ?? entry['16GB_min'] ?? null),
      borderColor: 'rgb(54, 162, 235)',
      backgroundColor: 'rgba(54, 162, 235, 0.1)',
      borderWidth: 2,
      pointRadius: 2,
      pointHoverRadius: 6,
      spanGaps: true,
      tension: 0.1,
      fill: false
    },
    {
      label: '16GB Avg (CZK)',
      data: historyData.map(entry => entry['16GB_avg'] ?? null),
      borderColor: 'rgb(54, 162, 235)',
      borderDash: [5, 5],
      borderWidth: 1.5,
      pointRadius: 1,
      pointHoverRadius: 5,
      spanGaps: true,
      tension: 0.1,
      fill: false
    },
    {
      label: '32GB Min (CZK)',
      data: historyData.map(entry => entry['32GB_datart'] ?? entry['32GB_min'] ?? null),
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.1)',
      borderWidth: 2,
      pointRadius: 2,
      pointHoverRadius: 6,
      spanGaps: true,
      tension: 0.1,
      fill: false
    },
    {
      label: '32GB Avg (CZK)',
      data: historyData.map(entry => entry['32GB_avg'] ?? null),
      borderColor: 'rgb(75, 192, 192)',
      borderDash: [5, 5],
      borderWidth: 1.5,
      pointRadius: 1,
      pointHoverRadius: 5,
      spanGaps: true,
      tension: 0.1,
      fill: false
    }
  ];

  const ctx = document.getElementById('chartDatart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: datasets
    },
    options: {
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        title: {
          display: true,
          text: 'Datart DDR5 RAM Price Trends'
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        y: { 
          beginAtZero: false,
          title: { display: true, text: 'Price (CZK)' }
        },
        x: {
          title: { display: true, text: 'Date' }
        }
      }
    }
  });
});
</script>

<hr>

{% if site.data.ram_prices %}
<p>Last updated: {{ site.data.ram_prices.last_updated }}</p>

{% for category in site.data.ram_prices.categories %}
  <h3>{{ category[0] }} DDR5 RAM</h3>
  <table>
    <thead>
      <tr>
        <th>Product Name</th>
        <th>Price (CZK)</th>
      </tr>
    </thead>
    <tbody>
      {% for item in category[1] %}
        <tr>
          <td><a href="{{ item.link }}">{{ item.name }}</a></td>
          <td>{{ item.price }} ,-</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
{% endfor %}

{% else %}
<p>No price data available yet. Please run the scraper.</p>
{% endif %}
