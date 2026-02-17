"""Scrape remote developer jobs from RemoteOK into a CSV file."""

import argparse
import csv
import time
from pathlib import Path
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

JobRecord = Dict[str, str]
OUTPUT_FIELDS = ["title", "company", "location", "salary", "url"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape remote developer jobs from RemoteOK and export to CSV."
    )
    parser.add_argument(
        "--base-url",
        default="https://remoteok.com/remote-dev-jobs",
        help="RemoteOK listing URL to scrape.",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="Number of listing pages to scrape (default: 1).",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=2.0,
        help="Seconds to wait between pages (default: 2).",
    )
    parser.add_argument(
        "--output",
        default="remote_jobs_selenium.csv",
        help="Output CSV path. Relative paths are resolved from this script folder.",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run Chrome in headed mode (browser window visible).",
    )
    return parser.parse_args()


def create_driver(headless: bool = True) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )

    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )


def extract_text(row: WebElement, selector: str) -> str:
    try:
        return row.find_element(By.CSS_SELECTOR, selector).text.strip()
    except Exception:
        return ""


def scrape_remoteok(driver: webdriver.Chrome, url: str) -> List[JobRecord]:
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.job, tr[data-id]")))

    time.sleep(2)

    rows = driver.find_elements(By.CSS_SELECTOR, "tr.job, tr[data-id][data-href]")
    print(f"[INFO] Found {len(rows)} job rows on: {url}")

    jobs: List[JobRecord] = []
    for row in rows:
        row_classes = row.get_attribute("class") or ""
        if "closed" in row_classes or "expand" in row_classes:
            continue

        data_href = row.get_attribute("data-href") or row.get_attribute("data-url") or ""
        job_url = f"https://remoteok.com{data_href}" if data_href.startswith("/") else ""

        record: JobRecord = {
            "title": extract_text(
                row,
                "td.company.position.company_and_position h2[itemprop='title'], "
                "h2[itemprop='title']",
            ),
            "company": extract_text(
                row,
                "td.company.position.company_and_position h3[itemprop='name'], "
                "h3[itemprop='name']",
            ),
            "location": extract_text(row, "div.location"),
            "salary": extract_text(row, "div.salary"),
            "url": job_url,
        }

        if not record["title"] and not record["company"]:
            continue

        jobs.append(record)

    print(f"[INFO] Extracted {len(jobs)} valid jobs from page.")
    return jobs


def scrape_multiple_pages(
    driver: webdriver.Chrome,
    base_url: str,
    pages: int = 1,
    sleep_seconds: float = 2.0,
) -> List[JobRecord]:
    all_jobs: List[JobRecord] = []
    seen_keys = set()

    for page in range(1, pages + 1):
        url = base_url if page == 1 else f"{base_url}?pg={page}"
        print(f"[INFO] Scraping page {page}/{pages}: {url}")

        page_jobs = scrape_remoteok(driver, url)
        print(f"[INFO] Page {page} returned {len(page_jobs)} jobs.")

        for job in page_jobs:
            dedupe_key = job["url"] or f'{job["title"]}::{job["company"]}'
            if dedupe_key in seen_keys:
                continue
            seen_keys.add(dedupe_key)
            all_jobs.append(job)

        if page < pages:
            time.sleep(sleep_seconds)

    print(f"[INFO] Total unique jobs collected: {len(all_jobs)}")
    return all_jobs


def save_to_csv(jobs: List[JobRecord], filename: str = "remote_jobs_selenium.csv") -> Path:
    output_path = Path(filename)
    if not output_path.is_absolute():
        script_dir = Path(__file__).parent.resolve()
        output_path = script_dir / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Writing CSV to: {output_path}")

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"[INFO] Saved {len(jobs)} rows.")
    return output_path


def main() -> None:
    args = parse_args()
    if args.pages < 1:
        raise ValueError("--pages must be at least 1.")

    driver = create_driver(headless=not args.headed)
    try:
        jobs = scrape_multiple_pages(
            driver=driver,
            base_url=args.base_url,
            pages=args.pages,
            sleep_seconds=args.sleep,
        )
        save_to_csv(jobs, args.output)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
