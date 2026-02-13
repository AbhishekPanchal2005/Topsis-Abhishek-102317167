# TOPSIS Implementation (Assignment)

**Submitted by:** Abhishek
**Roll Number:** 102317167

This repository contains the solution for the TOPSIS assignment, divided into three parts.

## Part 1: Command Line Script
A Python script to calculate TOPSIS scores from the command line.
- **File:** `topsis.py`
- **Usage:** `python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>`

## Part 2: PyPI Package
A custom Python library uploaded to PyPI to calculate TOPSIS scores.
- **PyPI Link:** https://pypi.org/project/topsis-abhishek-102317167/
- **Installation:** `pip install topsis-abhishek-102317167`
- **Usage:** `python -m topsis_abhishek_102317167 <InputDataFile> <Weights> <Impacts> <ResultFileName>`

## Part 3: Web Service
A Flask-based web application that accepts a CSV file and emails the results.
- **Folder:** `Web_Service`
- **How to run:**
  1. Navigate to the folder.
  2. Run `python app.py`.
  3. Open `http://127.0.0.1:5000/` in your browser.
