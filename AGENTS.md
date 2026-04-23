# Repository Guidelines

## Project Structure & Module Organization
This repository publishes a Japanese resume site with Jekyll and the Minimal Mistakes theme.

- `index.md`: main public resume page.
- `projects.md`: supporting project details.
- `_config.yml`: Jekyll and site metadata.
- `assets/css/main.scss`: site and print styling overrides.
- `scripts/export_single_page_pdf.mjs`: Playwright-based PDF export script.
- `dist/`: generated PDFs.
- `_site/`: generated static output; treat as build output, not source.
- `ref/`: working notes and reference material for edits.

## Build, Test, and Development Commands
- `docker compose up`: run the local Jekyll preview on `http://localhost:4000`.
- `bundle install`: install Ruby dependencies for local Jekyll usage.
- `bundle exec jekyll serve`: run the site locally without Docker.
- `node scripts/export_single_page_pdf.mjs http://localhost:4000 dist/takuma-yoshioka.pdf`: export the current page as A4 PDF.
- `node scripts/export_single_page_pdf.mjs --single-page http://localhost:4000 dist/resume-long.pdf`: export one long PDF page.

## Coding Style & Naming Conventions
Use concise Markdown with clear Japanese business writing. Keep headings stable because sidebar links and in-page anchors depend on them. In SCSS and JavaScript, follow the existing style:

- 2-space indentation.
- Prefer small, direct changes over broad refactors.
- Use descriptive file names such as `resume-long.pdf` and `export_single_page_pdf.mjs`.
- Preserve print-specific rules in `assets/css/main.scss` when adjusting layout.

## Testing Guidelines
There is no automated test suite in this repository. Validate changes by:

- running the local preview and checking `index.md` and `projects.md`,
- verifying print layout in browser print preview when CSS changes,
- regenerating PDFs after content or layout edits.

If you touch export logic, confirm the output file is created in `dist/` and opens correctly.

## Commit & Pull Request Guidelines
Recent history favors short, imperative commit messages, often scoped by file, for example:

- `index.md: update Flare成果記述`
- `resume updates and PDF export optimization`

Prefer one focused change per commit. For pull requests, include:

- a short summary of content or layout changes,
- affected files and output artifacts,
- screenshots or PDF samples for visual changes,
- linked issue or context when applicable.
