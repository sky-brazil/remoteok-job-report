"""Generate an Excel report from scraped RemoteOK job data."""

import argparse
from pathlib import Path

import pandas as pd

EXPECTED_COLUMNS = ["title", "company", "location", "salary", "url"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an Excel report from a RemoteOK jobs CSV file."
    )
    parser.add_argument(
        "--input",
        default="remote_jobs_selenium.csv",
        help="Input CSV path. Relative paths are resolved from this script folder.",
    )
    parser.add_argument(
        "--output",
        default="remote_jobs_report.xlsx",
        help="Output Excel path. Relative paths are resolved from this script folder.",
    )
    return parser.parse_args()


def resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return Path(__file__).parent.resolve() / path


def load_jobs(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    missing = sorted(set(EXPECTED_COLUMNS).difference(df.columns))
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")
    return df


def normalize_text(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.replace(r"\s+", " ", regex=True).str.strip()


def join_unique(values: pd.Series) -> str:
    unique_values = sorted({value for value in values if isinstance(value, str) and value})
    return ", ".join(unique_values)


def clean_jobs(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    for column in EXPECTED_COLUMNS:
        cleaned[column] = normalize_text(cleaned[column])

    cleaned = cleaned[(cleaned["title"] != "") & (cleaned["company"] != "")]
    cleaned["location"] = cleaned["location"].replace("", "Unspecified")
    cleaned = cleaned.drop_duplicates(
        subset=["title", "company", "location", "url"], keep="first"
    ).reset_index(drop=True)
    return cleaned


def summarize_by_company(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("company")
        .agg(
            jobs_count=("title", "count"),
            locations=("location", join_unique),
        )
        .reset_index()
        .sort_values(["jobs_count", "company"], ascending=[False, True])
    )


def summarize_by_location(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("location")
        .agg(
            jobs_count=("title", "count"),
            companies=("company", join_unique),
        )
        .reset_index()
        .sort_values(["jobs_count", "location"], ascending=[False, True])
    )


def write_report(df: pd.DataFrame, output_excel: Path) -> None:
    by_company = summarize_by_company(df)
    by_location = summarize_by_location(df)

    output_excel.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_excel, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Raw_Data", index=False)
        by_company.to_excel(writer, sheet_name="By_Company", index=False)
        by_location.to_excel(writer, sheet_name="By_Location", index=False)


def main() -> None:
    args = parse_args()
    csv_path = resolve_path(args.input)
    output_excel = resolve_path(args.output)

    print(f"[INFO] Loading data from: {csv_path}")
    cleaned_jobs = clean_jobs(load_jobs(csv_path))
    print(f"[INFO] Jobs after cleaning: {len(cleaned_jobs)}")

    print(f"[INFO] Writing report to: {output_excel}")
    write_report(cleaned_jobs, output_excel)
    print("[INFO] Excel report generated successfully.")


if __name__ == "__main__":
    main()
