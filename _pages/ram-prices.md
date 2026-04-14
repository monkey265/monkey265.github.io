---
permalink: /ram-prices/
title: "DDR5 RAM Price Tracker (Alza & Datart)"
---

This page displays the latest DDR5 RAM prices aggregated from Alza.cz and Datart.cz via the Hlídač Shopů API.

<!-- Chart.js setup -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; margin: 20px 0;">
  <div><canvas id="chart8GB"></canvas></div>
  <div><canvas id="chart16GB"></canvas></div>
  <div><canvas id="chart32GB"></canvas></div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const historyData = {{ site.data.ram_history | jsonify }};
  
  if (!historyData || historyData.length === 0) {
    document.querySelector('.grid').innerHTML = '<p>No history data available yet to render graphs.</p>';
    return;
  }

  const labels = historyData.map(entry => entry.date);

  function createChart(canvasId, category, color) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: `${category} Min (CZK)`,
            data: historyData.map(entry => entry[`${category}_min`]),
            borderColor: color,
            backgroundColor: color.replace('1)', '0.1)'),
            tension: 0.1,
            fill: false
          },
          {
            label: `${category} Avg (CZK)`,
            data: historyData.map(entry => entry[`${category}_avg`]),
            borderColor: color,
            borderDash: [5, 5],
            tension: 0.1,
            fill: false
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: `${category} DDR5 Trend`
          }
        },
        scales: {
          y: { beginAtZero: false }
        }
      }
    });
  }

  createChart('chart8GB', '8GB', 'rgba(255, 99, 132, 1)');
  createChart('chart16GB', '16GB', 'rgba(54, 162, 235, 1)');
  createChart('chart32GB', '32GB', 'rgba(75, 192, 192, 1)');
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
