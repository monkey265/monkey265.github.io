---
title: MathJax Graph
permalink: /mathjax/
author_profile: false
---

<!-- ✅ Add MathJax + TikZJax here -->
<script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']]
    }
  };
</script>
<script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>
<script async src="https://tikzjax.com/v1/tikzjax.js"></script>

# MathJax TikZ Graph Example

This graph is rendered client-side:

$$
\begin{tikzpicture}
  \node (A) at (0,0) [circle, draw] {A};
  \node (B) at (2,0) [circle, draw] {B};
  \node (C) at (1,1.5) [circle, draw] {C};

  \draw[->] (A) -- (B);
  \draw[->] (B) -- (C);
  \draw[->] (C) -- (A);
\end{tikzpicture}
$$
