# ATM ClinVar + gnomAD VUS Explorer

An educational bioinformatics application for exploring **ATM missense variants classified by ClinVar as germline variants of uncertain significance (VUS)** alongside population-frequency evidence from **gnomAD**.

The project demonstrates an end-to-end computational workflow:

**ClinVar filtering → exact GRCh38 variant identification → gnomAD integration → validated app dataset → Streamlit explorer**

> **Educational use only.**
>
> This project does not diagnose patients, reclassify variants, or provide clinical recommendations. It presents existing public evidence from ClinVar and gnomAD. Questions about a specific variant should be discussed with a qualified clinician or genetic counselor.

---

## Project Overview

Variants of uncertain significance do not currently have enough evidence to be confidently classified as pathogenic or benign.

This project explores one useful category of variant evidence: whether an ATM missense VUS appears in the gnomAD population database and, when available, its:

- Allele count
- Allele number
- Allele frequency
- Homozygote count
- gnomAD filter status

The application combines this population information with existing ClinVar annotations in a searchable and filterable interface.

---

## Current Results

The pipeline produced a final dataset containing:

| Result | Count |
|---|---:|
| Eligible ATM missense VUS candidates | 4,534 |
| Matched exactly in gnomAD | 1,474 |
| Not found in gnomAD | 3,060 |
| gnomAD match rate | 32.51% |
| Protein changes successfully parsed | 4,526 |
| Protein changes requiring review | 8 |

Variants were matched using exact GRCh38 genomic identities in the format:

```text
CHROM-POS-REF-ALT
```

Example:

```text
11-108227628-A-G
```

---

## Streamlit Application

The current application provides:

- Summary metrics for the complete dataset
- Search by:
  - Protein change
  - ClinVar Variation ID
  - rsID
  - VCV accession
  - Genomic variant ID
- Filters for:
  - gnomAD match status
  - ClinVar review status
  - Associated condition
  - gnomAD allele-frequency range
- A browsable results table
- Graceful handling of variants without gnomAD evidence

### Application Screenshot

A screenshot will be added after the application interface is finalized.

---

## Data Pipeline

### Phase 1 — ClinVar Filtering

The ClinVar variant summary dataset was filtered to retain records with:

- Gene: `ATM`
- Germline classification: `Uncertain significance`
- Molecular consequence: `missense variant`
- Valid rsID
- Available GRCh38 location
- Review status beginning with `criteria provided`

These filters produced the candidate set summarized in **Current Results** above.

Main outputs:

```text
data/processed/atm_missense_vus_all.csv
data/processed/atm_clinvar_candidates.csv
```

---

### Phase 2 — Exact GRCh38 Variant Identities

ClinVar Variation IDs were matched against the ClinVar GRCh38 VCF.

For every successfully resolved variant, the pipeline preserved:

- Chromosome
- Position
- Reference allele
- Alternate allele

These fields were used to construct exact genomic variant identifiers in the format:

```text
CHROM-POS-REF-ALT
```

Main output:

```text
data/processed/atm_candidates_with_variant_id.csv
```

---

### Phase 3 — gnomAD Integration

ATM variants were queried through the official gnomAD GraphQL API using gnomAD v4 GRCh38 data.

Retrieved fields included:

- Variant ID
- Allele count
- Allele number
- Homozygote count
- Filter status

Allele frequency was calculated as:

```text
gnomad_af = gnomad_ac / gnomad_an
```

Duplicate gnomAD variant IDs were removed before ClinVar and gnomAD records were joined through an exact match on `variant_id`. Match counts are listed in **Current Results** above.

Main outputs:

```text
data/processed/atm_clinvar_gnomad_enriched.csv
data/processed/atm_clinvar_gnomad_unmatched.csv
```

---

### Phase 4 — Application Dataset Assembly

Matched and unmatched records were combined into one app-facing dataset.

The following fields were extracted from ClinVar variation descriptions:

- Transcript
- HGVS coding notation
- HGVS protein notation

Protein changes such as `R3008C` were separated into:

- Reference amino acid
- Protein position
- Alternate amino acid

Records that could not be represented as simple amino-acid substitutions were marked as:

```text
Needs review
```

Additional app-facing fields include:

- ClinVar identifiers and annotations
- Genomic coordinates and alleles
- Transcript and HGVS notation
- Protein-change information
- gnomAD match status
- Allele count
- Allele number
- Allele frequency
- Homozygote count
- gnomAD filters
- Protein parsing status

Final output:

```text
data/processed/atm_vus_app_dataset.csv
```

---

### Phase 5 — Streamlit Explorer

The final dataset is loaded into the Streamlit app (see **Streamlit Application** above for features) through a dedicated `src/data_loader.py` module, keeping data loading separate from UI code so the app can focus on presentation and interaction rather than repeating the pipeline.

---

## Validation

The pipeline includes checks for:

- Unique and non-missing variant IDs
- Agreement between `variant_id` and separate genomic fields
- Non-negative allele counts
- Positive allele numbers
- Allele count not exceeding allele number
- Non-negative homozygote counts
- Allele frequencies between 0 and 1
- Unique normalized gnomAD variant IDs
- Matched and unmatched row counts summing to all candidates
- Final dataset row-count consistency
- Final identifier consistency
- Protein-change parsing status

These checks validate the internal consistency of the pipeline. They do not establish clinical validity.

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

- Python
- pandas
- Streamlit
- Jupyter Notebook
- ClinVar public genomic data
- ClinVar GRCh38 VCF
- gnomAD GraphQL API
- gnomAD v4
- GRCh38 genomic coordinates

---

## Limitations

- Absence from gnomAD does not imply that a variant is pathogenic.
- Presence in gnomAD does not independently establish that a variant is benign.
- Allele frequency is only one category of variant evidence.
- ClinVar classifications and review statuses may change over time.
- gnomAD data may change as newer releases become available.
- Complex protein changes may require manual review instead of simple amino-acid substitution parsing.
- The project currently focuses only on ATM missense variants classified as germline VUS.
- The application does not apply ACMG/AMP criteria.
- The application does not generate new clinical classifications.
- The application must not be used for medical decision-making.

---

## Project Status

The complete data pipeline and initial Streamlit application are functional.

The notebooks are currently being reviewed and independently rebuilt as part of the learning process. The goal is not only to produce a working application, but to understand and document every major transformation and design decision in the pipeline.

Planned improvements include:

- A detailed single-variant evidence view
- CSV download for filtered results
- Improved table formatting
- Application screenshots
- Streamlit deployment
- Additional notebook documentation
- Refactoring reusable processing functions
- Tests for filtering and parsing logic

---

## Learning Goals

This project was built to practise:

- Working with real public genomic datasets
- Understanding genomic variant identifiers
- Resolving ClinVar Variation IDs through a genomic VCF
- Constructing exact `CHROM-POS-REF-ALT` identifiers
- Combining clinical and population databases
- Querying a GraphQL API
- Cleaning and validating biological data
- Handling missing population evidence
- Designing reproducible notebook pipelines
- Building an interactive bioinformatics application
- Communicating scientific and clinical limitations responsibly

---

## Data Sources

This project uses publicly available data from:

- **ClinVar**, maintained by the National Center for Biotechnology Information
- **gnomAD**, maintained by the Genome Aggregation Database team

The original databases should be consulted for current records, documentation, licensing information, and usage conditions.

---

## Author

Built by **Pat**, a Computer Science undergraduate learning bioinformatics through project-based study.