---
title: "Příspěvky"
permalink: /posts/
layout: single
author_profile: true
---

<div class="entries-list">
  {% for post in site.posts %}
    {% include archive-single.html type="list" %}
  {% endfor %}
</div>
