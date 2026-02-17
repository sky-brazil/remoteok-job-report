# RemoteOK Job Intelligence Pipeline

A production-style Python portfolio project that demonstrates how to collect remote job listings and transform them into a business-ready Excel report for quick market analysis.

This repository is designed to showcase practical skills companies usually look for in freelance automation and data roles:

- Web scraping with Selenium
- Data cleaning and transformation with Pandas
- Structured reporting for non-technical stakeholders
- Reliable command-line workflows for repeatable execution

---

## Business Value

This project turns unstructured job board content into an organized dataset and summary report that can support:

- Hiring trend analysis
- Talent market scouting
- Compensation benchmarking (when salary data is available)
- Weekly reporting workflows for recruitment or operations teams

---

## Project Components

### 1) Scraper (`remote_jobs_scraper_selenium.py`)

Collects remote developer job postings from RemoteOK and saves structured output to CSV.

**Captured fields**
- Job title
- Company
- Location
- Salary (if present)
- Direct listing URL

**Highlights**
- Headless Chrome support (or headed mode when needed)
- Pagination support for multi-page scraping
- Consistent CSV output schema

### 2) Report Generator (`job_report_automation.py`)

Reads the scraped CSV, applies cleaning rules, and exports an Excel workbook with multiple sheets:

- `Raw_Data`
- `By_Company`
- `By_Location`

This enables fast handoff to business users, analysts, or dashboards.

---

## Tech Stack

- Python 3
- Selenium
- webdriver-manager
- Pandas
- XlsxWriter

---

## Quick Start

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### 2. Run the scraper

```bash
python remote_jobs_scraper_selenium.py --pages 1 --output remote_jobs_selenium.csv
```

Optional flags:

- `--headed` to run Chrome with UI
- `--sleep 2` to adjust delay between pages
- `--base-url` to target a different RemoteOK listing URL

### 3. Generate the Excel report

```bash
python job_report_automation.py --input remote_jobs_selenium.csv --output remote_jobs_report.xlsx
```

---

## Repository Structure

```text
.
├── remote_jobs_scraper_selenium.py   # Data collection
├── job_report_automation.py          # Data cleanup and Excel reporting
├── remote_jobs_selenium.csv          # Sample output dataset
├── remote_jobs_report.xlsx           # Sample Excel report
├── requirements.txt
└── README.md
```

---

## Professional Notes

- The codebase is intentionally small, readable, and easy to adapt for client projects.
- Naming, output schema, and workflow steps are structured for professional delivery.
- This repository can be extended with scheduling, cloud storage, and BI integrations.

---

## License

For portfolio and educational use. Add a formal license file if you plan to distribute or commercialize this code publicly.
