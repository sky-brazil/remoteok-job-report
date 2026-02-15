# RemoteOK Remote Jobs Automation (Scraper + Excel Report)

This repository contains a small automation pipeline in Python that:

1. Scrapes remote developer job listings from [RemoteOK](https://remoteok.com/remote-dev-jobs) using Selenium. [file:57]
2. Generates a business-friendly Excel report from the scraped CSV using Pandas.

It shows an end-to-end workflow: **web scraping → cleaned dataset → Excel report ready for dashboards or further automation**. [web:95][web:98]

---

## Project 1 – RemoteOK Job Scraper (Python + Selenium)

`remote_jobs_scraper_selenium.py`

### What it does

- Opens the RemoteOK “remote dev jobs” page in a real Chrome browser (headless Selenium). [file:57]
- Extracts, for each job:
  - Job title
  - Company name
  - Location
  - Salary (if available)
  - Direct job URL (built from `data-href`). [file:57]
- Supports simple pagination with a `pages_to_scrape` parameter.
- Saves the results to `remote_jobs_selenium.csv` in the same folder as the script. [web:15]

### Tech stack

- Python 3.x
- Selenium WebDriver
- `webdriver-manager` (automatic ChromeDriver management) [web:27]

### How to run the scraper

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv

   # Windows PowerShell
   .venv\Scripts\Activate.ps1

