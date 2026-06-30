---
name: software-copyright-from-source
description: Generate Chinese software copyright registration materials from an existing source tree and real product screenshots. Use when the user asks for 软著, 软件著作权, 申请表, 操作手册, 代码文档, 三件套, or wants to regenerate copyright PDFs using actual screenshots, source code excerpts, a reference application form PDF, and strict consistency between manual functions and source-code chapters.
---

# Software Copyright From Source

## Purpose

Create a reusable, evidence-based software copyright bundle:

- `申请表.pdf`
- `操作手册.pdf`
- `代码文档.pdf`

Use the real project source and real screenshots supplied by the user. Do not substitute mockups when the user asks for authentic screenshots.

## Core Workflow

1. Locate inputs:
   - Source tree, for example `/path/to/spec-action`.
   - Screenshot directory, for example `/path/to/软著/project/截图`.
   - Existing generated-output root, if any.
   - Optional reference application form PDF whose visual format should be followed.
2. Inspect the product screenshots and source layout before editing generated content.
3. Build a function map:
   - Order chapters by the operation manual flow.
   - Pair every screenshot with the function it actually shows.
   - Pair every manual function with matching source files and line ranges.
4. Generate:
   - Application form in bordered table style.
   - Operation manual with real screenshots, a cover, a table of contents, and usage steps only.
   - Code document with source excerpts ordered to match the manual.
5. Verify PDFs:
   - Render cover pages and representative content pages with `pdftoppm`.
   - Extract text with `pdftotext` and search for forbidden leftovers.
   - Copy final PDFs to `out/` with user-facing filenames.

## Non-Negotiable Content Rules

- Operation manual must explain how to use the system; do not mention source paths, code positions, corresponding source, or implementation excerpts.
- Code document may include source paths and line ranges, and its chapter order must match the manual's feature path.
- Screenshot captions and descriptions must match the actual screenshot content.
- Do not include boilerplate like `本文档源码直接摘自 ...`.
- Covers for all three PDFs must include version and `编写日期`.
- If the user provides a reference application form, match its structure and table style while adapting the content to the current software.
- Preserve user-requested naming and output directories.

## Application Form Rules

Keep the generated application form compatible with current online-entry constraints:

- Development hardware, runtime hardware, development OS, development tools, runtime platform, support software, development purpose, and target domain: 50 Chinese characters or fewer.
- Programming language: 120 characters or fewer.
- Main functions: 500-1300 characters.
- Technical characteristics: 100 characters or fewer.
- Source line count must be based on the actual source tree, excluding generated output, dependencies, build artifacts, screenshots, PDFs, and unrelated archives.

Use `application_profile` in the config to override these fields per project. Do not pad fields with irrelevant text; keep them concrete and consistent with the operation manual.

## Manual And Code Alignment

- Manual chapters should be pure user operation instructions: what the screen shows, what the user clicks or enters, and what result appears.
- Manual screenshots should appear near the section that describes them. If a figure floats into the wrong section, set `screenshots[].page_break_before` for the affected screenshot and regenerate.
- Code sections should prioritize source files that implement the same features shown in the manual screenshots.
- Keep code documents in the usual submission range of 60-80 pages unless the user asks otherwise. Prefer high-relevance excerpts over whole-project dumps.
- When reducing an oversized code document, remove low-relevance utilities, generated files, framework boilerplate, and duplicate styles first.
- When expanding an undersized code document, add closely related controllers, API clients, stores, route definitions, service logic, and component code that supports the same manual chapters.

## Scripted Generation

Use `scripts/generate_copyright_docs.py` for deterministic generation once the project map is known.

Example:

```bash
python3 ~/.codex/skills/software-copyright-from-source/scripts/generate_copyright_docs.py \
  --root /path/to/copyright-workdir \
  --source-root /path/to/project-source \
  --screenshots-dir /path/to/copyright-workdir/截图 \
  --config /path/to/copyright-workdir/copyright_config.json
```

The script writes intermediates to `manual_build/`, renders previews to `manual_build/preview/`, and copies final PDFs to `out/`.

Useful regeneration modes:

```bash
# Regenerate only the application form and validate field lengths.
python3 ~/.codex/skills/software-copyright-from-source/scripts/generate_copyright_docs.py \
  --root /path/to/copyright-workdir \
  --config /path/to/copyright-workdir/copyright_config.json \
  --only application

# Regenerate only the operation manual after screenshot or layout fixes.
python3 ~/.codex/skills/software-copyright-from-source/scripts/generate_copyright_docs.py \
  --root /path/to/copyright-workdir \
  --source-root /path/to/project-source \
  --screenshots-dir /path/to/copyright-workdir/截图 \
  --config /path/to/copyright-workdir/copyright_config.json \
  --only manual

# Regenerate only the code document and enforce the target page range.
python3 ~/.codex/skills/software-copyright-from-source/scripts/generate_copyright_docs.py \
  --root /path/to/copyright-workdir \
  --source-root /path/to/project-source \
  --config /path/to/copyright-workdir/copyright_config.json \
  --only code \
  --code-page-min 60 \
  --code-page-max 80
```

When only one PDF is regenerated, check that the existing `out/` folder still contains the other two final PDFs before packaging delivery materials.

## Delivery Packaging

For multiple software copyright projects under one root, collect only the final application materials into a clean delivery folder:

```bash
python3 ~/.codex/skills/software-copyright-from-source/scripts/collect_delivery.py \
  --root /path/to/软著 \
  --delivery-dir /path/to/软著/交付材料
```

The collector expects each project to contain exactly one `out/*_申请表.pdf`, one `out/*_操作手册.pdf`, and one `out/*_代码文档.pdf`. It creates one subfolder per software name, removes `.DS_Store`, and fails if non-PDF files remain in the delivery folder.

## Config

Create a JSON config in the target project. See `references/config-schema.md` for the supported shape.

Important fields:

- `software_name`: full display name on covers.
- `output_basename`: final Chinese filename stem.
- `version`, `completed_date`, `writing_date`.
- `source_line_total`: source-program total shown in the application form.
- `application_profile`: field-limited application-form text.
- `manual_profile`: overview, runtime environment, and common-issues text.
- `screenshots`: ordered screenshot metadata, descriptions, and operation steps.
- `code_sections`: ordered source excerpts that correspond to the manual chapters.

## Validation Checklist

Run these after generation:

```bash
pdftotext out/*_操作手册.pdf /tmp/manual.txt
rg -n "源码|源代码|代码位置|对应源码|本文档源码直接摘自|/Users/|src/" /tmp/manual.txt || true
pdftotext out/*_申请表.pdf /tmp/application.txt
rg -n "本文档源码直接摘自|代码位置|对应源码|/Users/" /tmp/application.txt || true
pdfinfo out/*.pdf | rg "^(Title|Pages)"
```

Render pages for visual inspection:

```bash
mkdir -p /tmp/copyright_preview
pdftoppm -png -f 1 -l 3 -r 140 out/*_申请表.pdf /tmp/copyright_preview/application
pdftoppm -png -f 1 -l 5 -r 140 out/*_操作手册.pdf /tmp/copyright_preview/manual
pdftoppm -png -f 1 -l 3 -r 140 out/*_代码文档.pdf /tmp/copyright_preview/code
```

If page layout is wrong, patch the config or script and regenerate instead of manually editing the PDFs.
