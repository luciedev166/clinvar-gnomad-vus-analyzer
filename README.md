# ClinVar + gnomAD VUS Analyzer

> **Status: In Progress**

A beginner-friendly bioinformatics project that explores variants of uncertain significance, or VUS, from the cancer-related **ATM gene** using public data from ClinVar and gnomAD.

## Project Overview

This project analyzes germline missense variants of uncertain significance from the ATM gene.

ClinVar data is cleaned and filtered using Python and pandas. A smaller selection of approximately 10–20 variants will later be compared with population-frequency data from gnomAD.

The collected evidence will be organized into a clear table and displayed through an interactive Streamlit web application.

## Project Goals

- Learn how ClinVar and gnomAD are used in bioinformatics
- Practice cleaning and filtering biological datasets with Python
- Build a reproducible variant evidence table
- Compare ClinVar interpretations with gnomAD population frequencies
- Create an interactive Streamlit application
- Explain genetic evidence clearly and responsibly

## Planned Outputs

- A Jupyter notebook for exploring and cleaning ClinVar data
- Python scripts for processing variant data
- A CSV evidence table containing selected ATM variants
- A Streamlit web application
- Documentation of the methods, findings, and limitations

## Project Structure

```text
clinvar-gnomad-vus-analyzer/
├── app.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_explore_clinvar.ipynb
├── src/
├── README.md
└── requirements.txt