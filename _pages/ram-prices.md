---
permalink: /ram-prices/
title: "DDR5 RAM Price Tracker (Alza.cz)"
---

This page displays the latest DDR5 RAM prices scraped daily from Alza.cz and visualizes price trends.

<!-- Chart.js setup -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<div style="width: 100%; margin: 20px 0;">
  <canvas id="ramPriceChart"></canvas>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const historyData = {{ site.data.ram_history | jsonify }};
  
  if (!historyData || historyData.length === 0) {
    document.getElementById('ramPriceChart').parentElement.innerHTML = '<p>No history data available yet to render graph.</p>';
    return;
  }

  const labels = historyData.map(entry => entry.date);
  const datasets = [
    {
      label: '8GB Lowest Price (CZK)',
      data: historyData.map(entry => entry['8GB']),
      borderColor: 'rgb(255, 99, 132)',
      tension: 0.1,
      fill: false
    },
    {
      label: '16GB Lowest Price (CZK)',
      data: historyData.map(entry => entry['16GB']),
      borderColor: 'rgb(54, 162, 235)',
      tension: 0.1,
      fill: false
    },
    {
      label: '32GB Lowest Price (CZK)',
      data: historyData.map(entry => entry['32GB']),
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1,
      fill: false
    }
  ];

  new Chart(document.getElementById('ramPriceChart'), {
    type: 'line',
    data: {
      labels: labels,
      datasets: datasets
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'DDR5 RAM Price Trends (Lowest per Category)'
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          title: {
            display: true,
            text: 'Price (CZK)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Date'
          }
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
