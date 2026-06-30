#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


MATERIAL_SUFFIXES = ("申请表", "操作手册", "代码文档")


def project_name_from(pdf_path: Path) -> str:
    stem = pdf_path.stem
    for suffix in MATERIAL_SUFFIXES:
        marker = f"_{suffix}"
        if stem.endswith(marker):
            return stem[: -len(marker)]
    return pdf_path.parent.parent.name


def find_project_dirs(root: Path) -> list[Path]:
    projects = []
    seen = set()
    for app_pdf in sorted(root.glob("*/out/*_申请表.pdf")):
        project_dir = app_pdf.parent.parent.resolve()
        if project_dir in seen:
            continue
        seen.add(project_dir)
        projects.append(project_dir)
    return projects


def material_files(project_dir: Path) -> dict[str, Path]:
    out_dir = project_dir / "out"
    result = {}
    for suffix in MATERIAL_SUFFIXES:
        matches = sorted(out_dir.glob(f"*_{suffix}.pdf"))
        if len(matches) != 1:
            raise FileNotFoundError(f"{project_dir}: expected one *_{suffix}.pdf, found {len(matches)}")
        result[suffix] = matches[0]
    return result


def collect_project(project_dir: Path, delivery_dir: Path) -> Path:
    files = material_files(project_dir)
    project_name = project_name_from(files["申请表"])
    target_dir = delivery_dir / project_name
    target_dir.mkdir(parents=True, exist_ok=True)
    for pdf_path in files.values():
        shutil.copy2(pdf_path, target_dir / pdf_path.name)
    return target_dir


def validate_delivery(delivery_dir: Path) -> None:
    for ds_store in delivery_dir.rglob(".DS_Store"):
        ds_store.unlink()
    non_pdfs = [path for path in delivery_dir.rglob("*") if path.is_file() and path.suffix.lower() != ".pdf"]
    if non_pdfs:
        listing = "\n".join(str(path) for path in non_pdfs)
        raise ValueError(f"交付目录包含非 PDF 文件:\n{listing}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect generated software copyright PDFs into a clean delivery folder.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root that contains project folders with out/*.pdf.")
    parser.add_argument("--delivery-dir", type=Path, required=True, help="Destination folder for grouped deliverables.")
    parser.add_argument("--projects", nargs="*", help="Optional project folder names or absolute paths. Defaults to auto-detection.")
    parser.add_argument("--no-clean", dest="clean", action="store_false", help="Do not remove the destination before collecting.")
    parser.set_defaults(clean=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    delivery_dir = args.delivery_dir.resolve()

    if args.clean and delivery_dir.exists():
        shutil.rmtree(delivery_dir)
    delivery_dir.mkdir(parents=True, exist_ok=True)

    if args.projects:
        project_dirs = [Path(item).expanduser() for item in args.projects]
        project_dirs = [(path if path.is_absolute() else root / path).resolve() for path in project_dirs]
    else:
        project_dirs = find_project_dirs(root)

    if not project_dirs:
        raise FileNotFoundError(f"未在 {root} 下找到 */out/*_申请表.pdf")

    targets = [collect_project(project_dir, delivery_dir) for project_dir in project_dirs]
    validate_delivery(delivery_dir)

    pdf_count = sum(1 for _ in delivery_dir.rglob("*.pdf"))
    print(f"delivery: {delivery_dir}")
    print(f"projects: {len(targets)}")
    print(f"pdfs: {pdf_count}")
    for target in targets:
        print(f"- {target}")


if __name__ == "__main__":
    main()
