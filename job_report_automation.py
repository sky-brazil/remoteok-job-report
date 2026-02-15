import pandas as pd
from pathlib import Path


def load_jobs(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    # garante colunas esperadas
    expected_cols = {"title", "company", "location", "salary", "url"}
    missing = expected_cols.difference(df.columns)
    if missing:
        raise ValueError(f"CSV is missing columns: {missing}")

    return df


def clean_jobs(df: pd.DataFrame) -> pd.DataFrame:
    # remove linhas totalmente vazias de título/empresa
    df = df.copy()
    df["title"] = df["title"].astype(str).str.strip()
    df["company"] = df["company"].astype(str).str.strip()
    df["location"] = df["location"].astype(str).str.strip()
    df["salary"] = df["salary"].astype(str).str.strip()

    df = df[(df["title"] != "") & (df["company"] != "")]
    return df


def summarize_by_company(df: pd.DataFrame) -> pd.DataFrame:
    by_company = (
        df.groupby("company")
        .agg(
            jobs_count=("title", "count"),
            locations=("location", lambda x: ", ".join(sorted(set(x)))),
        )
        .reset_index()
        .sort_values("jobs_count", ascending=False)
    )
    return by_company


def summarize_by_location(df: pd.DataFrame) -> pd.DataFrame:
    by_location = (
        df.groupby("location")
        .agg(
            jobs_count=("title", "count"),
            companies=("company", lambda x: ", ".join(sorted(set(x)))),
        )
        .reset_index()
        .sort_values("jobs_count", ascending=False)
    )
    return by_location


def main():
    script_dir = Path(__file__).parent.resolve()
    csv_path = script_dir / "remote_jobs_selenium.csv"
    output_excel = script_dir / "remote_jobs_report.xlsx"

    print(f"Lendo dados de: {csv_path}")
    df = load_jobs(csv_path)
    df = clean_jobs(df)

    print(f"Total de vagas após limpeza: {len(df)}")

    by_company = summarize_by_company(df)
    by_location = summarize_by_location(df)

    print(f"Salvando relatório em: {output_excel}")

    with pd.ExcelWriter(output_excel, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Raw_Data", index=False)
        by_company.to_excel(writer, sheet_name="By_Company", index=False)
        by_location.to_excel(writer, sheet_name="By_Location", index=False)

    print("Relatório Excel gerado com sucesso.")


if __name__ == "__main__":
    main()
