# ATM ClinVar + gnomAD VUS Explorer

An educational bioinformatics application for exploring **ATM missense variants classified by ClinVar as germline variants of uncertain significance (VUS)** alongside population-frequency evidence from **gnomAD**.

> **Educational use only.**
>
> This project does not diagnose patients, reclassify variants, or provide clinical recommendations. It presents existing public evidence from ClinVar and gnomAD. Questions about a specific variant should be discussed with a qualified clinician or genetic counselor.

---

## Project Overview

Variants of uncertain significance don't yet have enough evidence to be confidently classified as pathogenic or benign. This project explores one useful category of evidence: whether an ATM missense VUS appears in gnomAD and, when available, its allele count, allele number, allele frequency, homozygote count, and gnomAD filter status.

The pipeline goes **ClinVar filtering → exact GRCh38 variant identification → gnomAD integration → validated app dataset → Streamlit explorer**. Full pipeline details, including how variants were matched and validated, are documented in [`docs/PIPELINE.md`](docs/PIPELINE.md).

---

## Current Results

| Result | Count |
|---|---:|
| Eligible ATM missense VUS candidates | 4,534 |
| Matched exactly in gnomAD | 1,474 |
| Not found in gnomAD | 3,060 |
| gnomAD match rate | 32.51% |
| Protein changes successfully parsed | 4,526 |
| Protein changes requiring review | 8 |

Variants were matched using exact GRCh38 genomic identities (`CHROM-POS-REF-ALT`), e.g. `11-108227628-A-G`.

---

## Streamlit Application

- Summary metrics for the complete dataset
- Search by protein change, ClinVar Variation ID, rsID, VCV accession, or genomic variant ID
- Filters for gnomAD match status, ClinVar review status, associated condition, and gnomAD allele-frequency range
- A browsable results table
- Graceful handling of variants without gnomAD evidence

*Screenshot to be added once the interface is finalized.*

---

## Project Structure

```text
atm-clinvar-gnomad-vus-explorer/
├── app.py
├── src/
│   └── data_loader.py
├── notebooks/
│   ├── 01_explore_clinvar.ipynb
│   ├── 02_explore_gnomad.ipynb
│   ├── 03_explore_gnomad.ipynb
│   └── 04_build_app_dataset.ipynb
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   └── PIPELINE.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running the Application

### 1. Clone the repository

```bash
git clone https://github.com/your-username/atm-clinvar-gnomad-vus-explorer.git
cd atm-clinvar-gnomad-vus-explorer
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

---

## Main Technologies

Python, pandas, Streamlit, Jupyter Notebook, ClinVar public data and GRCh38 VCF, gnomAD GraphQL API (gnomAD v4), GRCh38 coordinates.

---

## Limitations

- Absence from gnomAD does not imply that a variant is pathogenic.
- Presence in gnomAD does not independently establish that a variant is benign.
- Allele frequency is only one category of variant evidence.
- ClinVar classifications and review statuses may change over time.
- gnomAD data may change as newer releases become available.
- Complex protein changes may require manual review instead of simple amino-acid substitution parsing.
- The project currently focuses only on ATM missense variants classified as germline VUS.
- The application does not apply ACMG/AMP criteria or generate new clinical classifications.
- The application must not be used for medical decision-making.

---

## Project Status

The complete data pipeline and initial Streamlit application are functional. The notebooks are being reviewed and rebuilt as part of the learning process, with a focus on documenting every major transformation and design decision.

Planned improvements:

- A detailed single-variant evidence view
- CSV download for filtered results
- Improved table formatting
- Application screenshots
- Streamlit deployment
- Additional notebook documentation
- Refactoring reusable processing functions
- Tests for filtering and parsing logic

---

## Data Sources

This project uses publicly available data from **ClinVar** (NCBI) and **gnomAD** (Genome Aggregation Database team). Consult the original databases for current records, documentation, licensing, and usage conditions.

---

## Author

Built by **Pat**, a Computer Science undergraduate learning bioinformatics through project-based study.
