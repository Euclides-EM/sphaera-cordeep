import argparse
from pathlib import Path
import re

import detect


DIAGRAMS_DIRNAME = "diagrams"
PDF_GLOB = "*.pdf"
VOL_SUFFIX_RE = re.compile(r"_vol\d+$", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("--file-list")
    return parser.parse_args()


def iter_pdfs(input_dir: Path) -> list[Path]:
    return sorted(path for path in input_dir.glob(PDF_GLOB) if path.is_file())


def normalize_pdf_name(value: str) -> str:
    name = Path(value).stem
    return VOL_SUFFIX_RE.sub("", name)


def load_allowed_names(file_list_path: Path | None) -> set[str] | None:
    if file_list_path is None:
        return None
    return {
        normalize_pdf_name(line.strip())
        for line in file_list_path.read_text().splitlines()
        if line.strip()
    }


def output_dir_for_pdf(pdf_path: Path, diagrams_dir: Path) -> Path:
    return diagrams_dir / pdf_path.stem


def run_detect(pdf_path: Path, output_dir: Path) -> None:
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    detect.run(
        source=str(pdf_path),
        project=str(output_dir.parent),
        name=output_dir.name,
        exist_ok=True,
        device="0"
    )


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir).resolve()
    diagrams_dir = input_dir / DIAGRAMS_DIRNAME
    file_list_path = Path(args.file_list).resolve() if args.file_list else None

    if not input_dir.is_dir():
        raise SystemExit(f"Input directory does not exist: {input_dir}")
    if file_list_path and not file_list_path.is_file():
        raise SystemExit(f"File list does not exist: {file_list_path}")

    allowed_names = load_allowed_names(file_list_path)

    for pdf_path in iter_pdfs(input_dir):
        if allowed_names is not None and normalize_pdf_name(pdf_path.name) not in allowed_names:
            continue
        output_dir = output_dir_for_pdf(pdf_path, diagrams_dir)
        if output_dir.exists():
            print(f"Skipping {pdf_path.name}: output already exists at {output_dir}")
            continue
        run_detect(pdf_path, output_dir)


if __name__ == "__main__":
    main()
