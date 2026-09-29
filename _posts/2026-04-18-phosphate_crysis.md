---
title: "Nadcházející fosfátová krize"
published: true
date: 2026-04-18T15:34:30-04:00
categories:
  - blog
tags:
  - Jekyll
  - update
---

Když si člověk dnes představí globální velmoc, téměř každý si představí
Spojené státy americké, Čínu, Rusko, Evropu a někdo i předestírá Afriku.

Budoucnost však leží v rukou jiné země - Maroka.

## Současný cyklus hnojiv

Rostliná produkce vyžaduje primární makroživiny, dusík, fosfor a draslík.

<div id="vis-phosphate-map" style="width: 100%; max-width: 900px; margin: 1.5em auto; overflow-x: auto;"></div>

<script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
<script>
const vegaSpec = {
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "description": "Světová naleziště fosfátových hornin (aktivní vs. potenciální zdroje).",
  "width": 800,
  "height": 450,
  "autosize": "fit",
  "projections": [
    {
      "name": "projection",
      "type": "equalEarth",
      "scale": 140,
      "translate": [
        {"signal": "width / 2"},
        {"signal": "height / 2"}
      ]
    }
  ],
  "scales": [
    {
      "name": "colorScale",
      "type": "ordinal",
      "domain": [
        "Aktivní / Prokázaná těžba",
        "Potenciální / Nové / Podmořské ložisko"
      ],
      "range": ["#e64a19", "#0097a7"]
    }
  ],
  "legends": [
    {
      "fill": "colorScale",
      "title": "Klasifikace ložisek fosforu",
      "orient": "bottom-left",
      "offset": 10,
      "padding": 6,
      "fillColor": "#ffffffea",
      "strokeColor": "#cccccc",
      "labelFontSize": 11,
      "titleFontSize": 12,
      "encode": {
        "symbols": {
          "update": {
            "shape": {"value": "circle"},
            "stroke": {"value": "#ffffff"},
            "strokeWidth": {"value": 1}
          }
        }
      }
    }
  ],
  "data": [
    {
      "name": "world",
      "url": "https://vega.github.io/vega-datasets/data/world-110m.json",
      "format": {
        "type": "topojson",
        "feature": "countries"
      }
    },
    {
      "name": "graticule",
      "transform": [
        { "type": "graticule" }
      ]
    },
    {
      "name": "deposits",
      "values": [
        {
          "name": "Khouribga & Ganntour (Oulad Abdoun)",
          "country": "Maroko",
          "lon": -6.9,
          "lat": 32.88,
          "status": "Aktivní / Prokázaná těžba",
          "size": 380,
          "details": "Největší světová sedimentární ložiska (>70 % globálních známých zásob)."
        },
        {
          "name": "Bou Craa",
          "country": "Západní Sahara",
          "lon": -12.85,
          "lat": 27.08,
          "status": "Aktivní / Prokázaná těžba",
          "size": 220,
          "details": "Strategický povrchový důl s pásovým dopravníkem k pobřeží Atlantiku."
        },
        {
          "name": "Dianchi / Kunming",
          "country": "Čína (Jün-nan)",
          "lon": 102.7,
          "lat": 24.9,
          "status": "Aktivní / Prokázaná těžba",
          "size": 240,
          "details": "Klíčové těžiště čínské produkce fosfátových hnojiv."
        },
        {
          "name": "Yichang",
          "country": "Čína (Chu-pej)",
          "lon": 111.3,
          "lat": 30.7,
          "status": "Aktivní / Prokázaná těžba",
          "size": 200,
          "details": "Masivní sedimentární pánve střední Číny."
        },
        {
          "name": "Bone Valley (Florida)",
          "country": "USA",
          "lon": -81.9,
          "lat": 27.8,
          "status": "Aktivní / Prokázaná těžba",
          "size": 180,
          "details": "Historické těžiště USA; ložiska nízkokadmiové rudy jsou v pokročilém stádiu vyčerpání."
        },
        {
          "name": "Aurora (Severní Karolína)",
          "country": "USA",
          "lon": -76.8,
          "lat": 35.3,
          "status": "Aktivní / Prokázaná těžba",
          "size": 150,
          "details": "Významný povrchový důl a chemický uzel společnosti Nutrien."
        },
        {
          "name": "Western Phosphate Field",
          "country": "USA (Idaho/Utah)",
          "lon": -111.4,
          "lat": 42.7,
          "status": "Aktivní / Prokázaná těžba",
          "size": 140,
          "details": "Formace Phosphoria s vyššími náklady na těžbu."
        },
        {
          "name": "Chibiny (Poloostrov Kola)",
          "country": "Rusko",
          "lon": 33.7,
          "lat": 67.6,
          "status": "Aktivní / Prokázaná těžba",
          "size": 240,
          "details": "Magmatický apatit mimořádné čistoty (téměř bez kadmia)."
        },
        {
          "name": "Wa'ad Al Shamal & Al Jalamid",
          "country": "Saúdská Arábie",
          "lon": 39.9,
          "lat": 31.3,
          "status": "Aktivní / Prokázaná těžba",
          "size": 220,
          "details": "Moderní státem dotovaný průmyslový komplex Ma'aden."
        },
        {
          "name": "Eshidiya",
          "country": "Jordánsko",
          "lon": 36.1,
          "lat": 29.9,
          "status": "Aktivní / Prokázaná těžba",
          "size": 170,
          "details": "Páteřní exportní zdroj Jordánska u přístavu Akaba."
        },
        {
          "name": "Abu Tartur",
          "country": "Egypt",
          "lon": 30.0,
          "lat": 25.5,
          "status": "Aktivní / Prokázaná těžba",
          "size": 150,
          "details": "Velké zásoby sedimentárního fosforitu v egyptské Západní poušti."
        },
        {
          "name": "Gafsa",
          "country": "Tunisko",
          "lon": 8.8,
          "lat": 34.4,
          "status": "Aktivní / Prokázaná těžba",
          "size": 130,
          "details": "Tradiční ložiska spravovaná státní společností CPG."
        },
        {
          "name": "Siilinjärvi",
          "country": "Finsko",
          "lon": 27.7,
          "lat": 63.1,
          "status": "Aktivní / Prokázaná těžba",
          "size": 110,
          "details": "Jediný aktivní fosfátový důl v EU (karbonatitový komplex s čistým apatitem, Yara)."
        },
        {
          "name": "Araxá & Tapira",
          "country": "Brazílie",
          "lon": -46.9,
          "lat": -19.6,
          "status": "Aktivní / Prokázaná těžba",
          "size": 160,
          "details": "Zvětralé karbonatity pro brazilský zemědělský sektor."
        },
        {
          "name": "Bayóvar (Sechura)",
          "country": "Peru",
          "lon": -80.8,
          "lat": -5.8,
          "status": "Aktivní / Prokázaná těžba",
          "size": 150,
          "details": "Mladé sedimentární ložisko s nízkými těžebními náklady u Pacifiku."
        },
        {
          "name": "Phalaborwa",
          "country": "Jihoafrická republika",
          "lon": 31.1,
          "lat": -23.9,
          "status": "Aktivní / Prokázaná těžba",
          "size": 140,
          "details": "Magmatická tělesa těžená spolu s mědí a vermikulitem."
        },
        {
          "name": "Phosphate Hill (Georgina)",
          "country": "Austrálie",
          "lon": 139.9,
          "lat": -21.9,
          "status": "Aktivní / Prokázaná těžba",
          "size": 130,
          "details": "Vnitrozemská ložiska v Queenslandu pro výrobu amonných fosfátů."
        },
        {
          "name": "Rogaland (Norge Mining)",
          "country": "Norsko",
          "lon": 6.0,
          "lat": 58.4,
          "status": "Potenciální / Nové / Podmořské ložisko",
          "size": 340,
          "details": "Hlubinná magmatická intruze; odhad až 70 mld. tun rudy (apatit + vanad + titan)."
        },
        {
          "name": "Per Geijer (Kiruna)",
          "country": "Švédsko",
          "lon": 20.2,
          "lat": 67.85,
          "status": "Potenciální / Nové / Podmořské ložisko",
          "size": 160,
          "details": "Ložisko LKAB; fosfor jako vedlejší produkt těžby magnetitu a vzácných zemin."
        },
        {
          "name": "Novopoltavka",
          "country": "Ukrajina",
          "lon": 36.2,
          "lat": 47.2,
          "status": "Potenciální / Nové / Podmořské ložisko",
          "size": 130,
          "details": "Apatit-karbonatitové těleso v Záporožské oblasti."
        },
        {
          "name": "Sandpiper (Offshore)",
          "country": "Namibie (šelf)",
          "lon": 14.0,
          "lat": -23.5,
          "status": "Potenciální / Nové / Podmořské ložisko",
          "size": 180,
          "details": "Mořské fosfátové písky na kontinentálním šelfu."
        },
        {
          "name": "Chatham Rise (Offshore)",
          "country": "Nový Zéland",
          "lon": -179.5,
          "lat": -43.5,
          "status": "Potenciální / Nové / Podmořské ložisko",
          "size": 170,
          "details": "Hlubokomořské noduly v hloubce cca 400 metrů."
        },
        {
          "name": "Don Diego (Offshore)",
          "country": "Mexiko (Baja California)",
          "lon": -112.5,
          "lat": 25.0,
          "status": "Potenciální / Nové / Podmořské ložisko",
          "size": 150,
          "details": "Pobřežní mořské sedimenty v zálivu Ulloa."
        },
        {
          "name": "Hinda",
          "country": "Republika Kongo",
          "lon": 12.0,
          "lat": -4.7,
          "status": "Potenciální / Nové / Podmořské ložisko",
          "size": 140,
          "details": "Rozsáhlé nerozvinuté povrchové ložisko v subsaharské Africe."
        },
        {
          "name": "Karatau (rozvoj hlubinných vrstev)",
          "country": "Kazachstán",
          "lon": 70.5,
          "lat": 43.5,
          "status": "Potenciální / Nové / Podmořské ložisko",
          "size": 160,
          "details": "Fosforitová pánev s významnými zásobami pro hlubinnou těžbu."
        }
      ],
      "transform": [
        {
          "type": "geopoint",
          "projection": "projection",
          "fields": ["lon", "lat"]
        },
        {
          "type": "filter",
          "expr": "isValid(datum.x) && isValid(datum.y)"
        }
      ]
    }
  ],
  "marks": [
    {
      "type": "shape",
      "from": {"data": "graticule"},
      "encode": {
        "update": {
          "strokeWidth": {"value": 0.6},
          "stroke": {"value": "#e0e0e0"},
          "fill": {"value": null}
        }
      },
      "transform": [
        { "type": "geoshape", "projection": "projection" }
      ]
    },
    {
      "type": "shape",
      "from": {"data": "world"},
      "encode": {
        "update": {
          "strokeWidth": {"value": 0.8},
          "stroke": {"value": "#ffffff"},
          "fill": {"value": "#34495e"},
          "zindex": {"value": 0}
        },
        "hover": {
          "stroke": {"value": "#e74c3c"},
          "strokeWidth": {"value": 1.5},
          "zindex": {"value": 1}
        }
      },
      "transform": [
        { "type": "geoshape", "projection": "projection" }
      ]
    },
    {
      "type": "symbol",
      "from": {"data": "deposits"},
      "encode": {
        "update": {
          "x": {"field": "x"},
          "y": {"field": "y"},
          "size": {"field": "size"},
          "fill": {"scale": "colorScale", "field": "status"},
          "stroke": {"value": "#ffffff"},
          "strokeWidth": {"value": 1.5},
          "opacity": {"value": 0.9},
          "tooltip": {
            "signal": "{'Lokalita': datum.name, 'Země': datum.country, 'Status': datum.status, 'Geologický význam': datum.details}"
          },
          "zindex": {"value": 2}
        },
        "hover": {
          "stroke": {"value": "#ffeb3b"},
          "strokeWidth": {"value": 3},
          "opacity": {"value": 1}
        }
      }
    }
  ]
};

vegaEmbed('#vis-phosphate-map', vegaSpec, {
  renderer: 'svg',
  actions: false
});
</script>

<noscript>
  <p><a href="/assets/images/phosphate_deposits.svg"><img src="/assets/images/phosphate_deposits.svg" alt="mapa nalezišt fosforu"></a></p>
</noscript>

[1](https://www.fluencecorp.com/the-impending-phosphorus-crisis/)
