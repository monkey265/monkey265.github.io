---
title: "Hory"
permalink: /hory/
author_profile: false

zamyslene:
  - hora: "Säuleck"
    uiaa: "I"
    vzdalenost: "~510 km"
    charakter: "Dlouhý výstup údolím Dösental, v závěru balvany a lehký hřeben"
    zajimavost: "„Dámská třítisícovka“ pro svou snadnost, krásné jezero Dösener See"

  - hora: "Habicht"
    uiaa: "I"
    vzdalenost: "~540 km"
    charakter: "Skalnatý strmý terén přes Innsbrucker Hütte, jištěno lany a kramlemi"
    zajimavost: "Dominantní pyramida, dříve mylně považována za nejvyšší horu Tyrolska"

  - hora: "Schönbichler Horn"
    uiaa: "I"
    vzdalenost: "~510 km"
    charakter: "Součást Berliner Höhenweg, kamenitý hřeben zajištěný lany"
    zajimavost: "Nejvyšší bod slavného treku Berliner Höhenweg s výhledem na ledovce"

  - hora: "Hoher Sonnblick"
    uiaa: "I"
    vzdalenost: "~490 km"
    charakter: "Z údolí Rauris přes Rojacher Hütte, skalní hřebínek (místy lano / firn)"
    zajimavost: "Na vrcholu slavná observatoř z r. 1886 a chata Zittelhaus"
---

# Absolvované treky

- [Grosses Wiesbachhorn](https://jcada.cz/grosses-wiesbachhorn/)

# Zamýšlené

<table>
  <thead>
    <tr>
      <th>Hora</th>
      <th style="text-align: center;">UIAA</th>
      <th style="text-align: center;">Vzdálenost od Prahy</th>
      <th>Charakter trasy</th>
      <th>Zajímavost</th>
    </tr>
  </thead>
  <tbody>
    {% for h in page.zamyslene %}
    <tr>
      <td><strong>{{ h.hora }}</strong></td>
      <td style="text-align: center;">{{ h.uiaa }}</td>
      <td style="text-align: center;">{{ h.vzdalenost }}</td>
      <td>{{ h.charakter }}</td>
      <td>{{ h.zajimavost }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>