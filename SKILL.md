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

## Config

Create a JSON config in the target project. See `references/config-schema.md` for the supported shape.

Important fields:

- `software_name`: full display name on covers.
- `output_basename`: final Chinese filename stem.
- `version`, `completed_date`, `writing_date`.
- `source_line_total`: source-program total shown in the application form.
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
