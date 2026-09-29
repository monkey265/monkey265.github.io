---
permalink: /ram-prices/
title: "DDR5 RAM Price Tracker (Datart)"
classes: wide
---

This page displays the latest DDR5 RAM prices from Datart.cz.

<!-- Vega-Lite interactive chart -->
<script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>

<div id="vis-ram-prices" style="width: 100%; margin: 1.5em 0 0.5em 0; overflow-x: auto;"></div>
<div style="font-size: 0.85em; color: #555; text-align: center; margin-bottom: 2em; background: #f8f9fa; padding: 6px 14px; border-radius: 4px; border: 1px solid #e2e8f0;">
  💡 <strong>Interaktivní graf:</strong> Tažením myši ve spodním náhledu vyberete časové období. Kliknutím na položku v legendě zvýrazníte vybranou kapacitu RAM.
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const historyData = {{ site.data.ram_history | jsonify }};
  
  if (!historyData || historyData.length === 0) {
    document.getElementById('vis-ram-prices').innerHTML = '<p>No history data available yet to render graphs.</p>';
    return;
  }

  const tidyData = [];
  historyData.forEach(entry => {
    const d = entry.date;
    const v8_min = entry['8GB_datart'] ?? entry['8GB_min'];
    const v8_avg = entry['8GB_avg'];
    const v16_min = entry['16GB_datart'] ?? entry['16GB_min'];
    const v16_avg = entry['16GB_avg'];
    const v32_min = entry['32GB_datart'] ?? entry['32GB_min'];
    const v32_avg = entry['32GB_avg'];

    if (v8_min != null) tidyData.push({ date: d, capacity: '8GB', metric: 'Min', price: Number(v8_min) });
    if (v8_avg != null) tidyData.push({ date: d, capacity: '8GB', metric: 'Průměr', price: Number(v8_avg) });
    if (v16_min != null) tidyData.push({ date: d, capacity: '16GB', metric: 'Min', price: Number(v16_min) });
    if (v16_avg != null) tidyData.push({ date: d, capacity: '16GB', metric: 'Průměr', price: Number(v16_avg) });
    if (v32_min != null) tidyData.push({ date: d, capacity: '32GB', metric: 'Min', price: Number(v32_min) });
    if (v32_avg != null) tidyData.push({ date: d, capacity: '32GB', metric: 'Průměr', price: Number(v32_avg) });
  });

  const vlSpec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"values": tidyData},
    "vconcat": [
      {
        "width": "container",
        "height": 340,
        "title": {
          "text": "Vývoj cen DDR5 RAM (Datart.cz)",
          "fontSize": 15,
          "anchor": "start"
        },
        "transform": [{"filter": {"param": "brush"}}],
        "layer": [
          {
            "params": [
              {
                "name": "capacitySelect",
                "select": {"type": "point", "fields": ["capacity"]},
                "bind": "legend"
              }
            ],
            "mark": {
              "type": "line",
              "point": {"size": 20},
              "interpolate": "monotone"
            },
            "encoding": {
              "x": {
                "field": "date",
                "type": "temporal",
                "title": "Datum",
                "axis": {"format": "%d. %m. %Y", "grid": true}
              },
              "y": {
                "field": "price",
                "type": "quantitative",
                "title": "Cena (Kč)",
                "scale": {"zero": false},
                "axis": {"grid": true}
              },
              "color": {
                "field": "capacity",
                "type": "nominal",
                "title": "Kapacita",
                "scale": {
                  "domain": ["8GB", "16GB", "32GB"],
                  "range": ["#e74c3c", "#3498db", "#2ecc71"]
                }
              },
              "strokeDash": {
                "field": "metric",
                "type": "nominal",
                "title": "Metrika",
                "scale": {
                  "domain": ["Min", "Průměr"],
                  "range": [[1, 0], [5, 4]]
                }
              },
              "opacity": {
                "condition": {"param": "capacitySelect", "value": 1},
                "value": 0.15
              },
              "tooltip": [
                {"field": "date", "type": "temporal", "title": "Datum", "format": "%d. %m. %Y"},
                {"field": "capacity", "type": "nominal", "title": "Kapacita"},
                {"field": "metric", "type": "nominal", "title": "Typ ceny"},
                {"field": "price", "type": "quantitative", "title": "Cena", "format": ",.0f"}
              ]
            }
          }
        ]
      },
      {
        "width": "container",
        "height": 60,
        "title": {
          "text": "Výběr časového rozsahu (táhněte pro filtr)",
          "fontSize": 12,
          "anchor": "start",
          "color": "#666"
        },
        "mark": {"type": "line", "interpolate": "monotone"},
        "params": [
          {"name": "brush", "select": {"type": "interval", "encodings": ["x"]}}
        ],
        "encoding": {
          "x": {
            "field": "date",
            "type": "temporal",
            "title": null,
            "axis": {"format": "%b %Y"}
          },
          "y": {
            "field": "price",
            "type": "quantitative",
            "axis": null,
            "scale": {"zero": false}
          },
          "color": {
            "field": "capacity",
            "type": "nominal",
            "legend": null,
            "scale": {
              "domain": ["8GB", "16GB", "32GB"],
              "range": ["#e74c3c", "#3498db", "#2ecc71"]
            }
          }
        }
      }
    ]
  };

  vegaEmbed('#vis-ram-prices', vlSpec, {
    renderer: 'svg',
    actions: {export: true, source: false, compiled: false, editor: false}
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
