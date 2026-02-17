# Main Release Checklist

Use this checklist before merging into `main` to keep quality, traceability, and client-facing professionalism.

## 1) Scope and Messaging

- [ ] All user-facing text is in professional English.
- [ ] README reflects current behavior and command usage.
- [ ] Changelog includes all meaningful updates.
- [ ] PR summary explains business value and technical impact.

## 2) Code Quality

- [ ] No debug-only code or temporary TODO stubs remain.
- [ ] Naming is clear and commercially presentable.
- [ ] No secrets, tokens, or local credentials are committed.
- [ ] Python files compile successfully.

```bash
python3 -m py_compile remote_jobs_scraper_selenium.py job_report_automation.py
```

## 3) Functional Validation

- [ ] Scraper CLI help renders successfully.
- [ ] Report generator runs against sample CSV without errors.
- [ ] Output files are created in expected locations.

```bash
python3 remote_jobs_scraper_selenium.py --help
python3 job_report_automation.py --input remote_jobs_selenium.csv --output /tmp/remote_jobs_report_test.xlsx
```

## 4) Repository Hygiene

- [ ] `.gitignore` covers local cache/environment artifacts.
- [ ] Working tree is clean after tests (`git status`).
- [ ] Commit messages are clear and descriptive.
- [ ] Branch is pushed to origin and up to date.

## 5) Merge Confidence

- [ ] Risk level is documented in PR.
- [ ] Any manual follow-up steps are listed.
- [ ] Reviewer can reproduce results from README and commands above.

