# Jekyll Cheat Sheet & Rules

Quick reference for Jekyll and the Minimal Mistakes theme formatting and syntax.

---

## 1. Post & Page Conventions

### File Naming
- **Posts** go into `_posts/` with the filename format: `YYYY-MM-DD-title-slug.md` (e.g., `2026-09-22-my-post.md`).
- **Pages** go into `_pages/` (or root) with standard `.md` naming.

### Front Matter
Every file must start with YAML front matter:

```yaml
---
title: "Post Title"
date: 2026-09-22T19:30:00+02:00
last_modified_at: 2026-09-22T20:00:00+02:00
layout: single
categories:
  - blog
tags:
  - guide
  - jekyll
excerpt: "Brief summary for post lists."
toc: true
toc_label: "Table of Contents"
toc_sticky: true
---
```

---

## 2. Notices & Callout Boxes (Kramdown)

Append `{: .notice--<type>}` immediately below a paragraph:

```markdown
**Default Notice:** Simple informational callout box.
{: .notice}

**Primary Notice:** Primary accent styled notice.
{: .notice--primary}

**Info Notice:** Blue info style box.
{: .notice--info}

**Warning Notice:** Yellow/orange warning box.
{: .notice--warning}

**Danger Notice:** Red alert/danger box.
{: .notice--danger}

**Success Notice:** Green confirmation box.
{: .notice--success}
```

---

## 3. Excerpts & Read More

Split content for blog post previews using `<!--more-->`:

```markdown
First paragraph visible in archive previews.

<!--more-->

Remaining content only visible on the full post page.
```

---

## 4. Code Blocks & Highlighting

Fenced code blocks with language syntax highlighting:

````markdown
```ruby
def hello(name)
  puts "Hello, #{name}!"
end
```

```bash
bundle exec jekyll serve
```
````

---

## 5. Blockquotes & Citations

```markdown
> This is a quote from an author.
> <cite><a href="https://example.com">Author Name</a></cite>
```

---

## 6. Liquid Tags & Captures

Capture markdown/HTML blocks and render them with Liquid:

```html
{% capture my_notice %}
#### Title
* Bullet point 1
* Bullet point 2
{% endcapture %}

<div class="notice--info">{{ my_notice | markdownify }}</div>
```

To display raw Liquid tags without executing them:

```liquid
{% raw %}
{{ variable }}
{% endraw %}
```

---

## 7. Useful CLI Commands

```bash
# Install dependencies
bundle install

# Run local development server
bundle exec jekyll serve

# Run with drafts & live reload
bundle exec jekyll serve --drafts --livereload
```
