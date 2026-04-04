import argparse
from pathlib import Path

import detect


DIAGRAMS_DIRNAME = "diagrams"
PDF_GLOB = "*.pdf"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    return parser.parse_args()


def iter_pdfs(input_dir: Path) -> list[Path]:
    return sorted(path for path in input_dir.glob(PDF_GLOB) if path.is_file())


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

    if not input_dir.is_dir():
        raise SystemExit(f"Input directory does not exist: {input_dir}")

    for pdf_path in iter_pdfs(input_dir):
        output_dir = diagrams_dir / pdf_path.stem
        if output_dir.is_dir():
            continue
        run_detect(pdf_path, output_dir)


if __name__ == "__main__":
    main()
