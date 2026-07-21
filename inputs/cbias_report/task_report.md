# Symposium Attendee Analysis - Exploratory Task

## Objective

Analyse data consisting of a series of CSV and TXT files, describing lists of attendees, abstract submissions,
and attendee feedback for a series of symposia. The aim is to explore the data and answer key questions about
year-to-year trends. Generate metrics and visualisations that provide insight and would be informative to key
stakeholders, such as the organising committee, life scientists, industry partners, funders, developers of bioimage
analysis software, and other stakeholders.

## Input

A parent directory, containing subdirectories, each with data for one of four specific years (2022-2025 inclusive). The
data consists of:

- **Attendees**: one CSV per year (`CBIAS_<year>_Attendees.csv`), one row per registration, including a ticket
  type/category (e.g. Academic, Industry, Online Only, Sponsors).
- **Feedback**: one CSV per year, one row per respondent, columns are the survey questions asked that year.
- **Abstracts**: one subfolder per year (`<year>_Abstracts`), each containing one plain-text file per submission
  (`<n>_Abstract.txt`) with `Label: value` fields (title, abstract text, keywords, etc.).

Note: file formats, column names, and field labels are not perfectly consistent across all four years – handle
missing/renamed fields gracefully rather than assuming an identical schema every year.

## Guiding Questions for Analysis

Your analysis should help answer these exploratory questions:

1. **Attendee Demographics**: Does the demographic description of attendees change over time? If so, how?
2. **Abstract Content**: Does the language used in abstract submissions change over time? If so, how?
3. **Feedback**: Do common themes emerge in attendee feedback? Do they change over time?
4. **Programs**: Review the symposia programs (available at https://www.crick.ac.uk/whats-on/crick-bioimage-analysis-symposium-20##) to identify key topics and trends and correlations with abstract content and attendee demographics. Does this change over time?
5. **Stakeholders**: Do attendees fall into distinct stakeholder groups (life scientist, software developer, funder, etc.) or is there evidence of these boundaries being blurred? Is there evidence of increased collaboration post-attendance?

## Analysis Requirements

### 1. Suggest Key metrics

Analyse the input data and suggest **key metrics** that help answer the guiding questions above. Choose
metrics that are:

- Computable from the available data
- Relevant to at least one of the guiding questions

Avoid anything already suggested in this GitHub repo: https://github.com/djpbarry/cbias-survey

### 2. Create Visualisations (PNG files)

Create visualisations that illustrate the metrics chosen in section 1. Pick visualisations that help answer the guiding 
questions and would be easily interpretable by all stakeholders.

### 3. Identify Data Gaps

After analysis, make specific suggestions for additional data/fields that would improve future analysis:

- Focus on what data would help answer the guiding questions more clearly
- Format: Bulleted list with a brief explanation of why each would be useful

## Output Requirements

Generate a Python script to conduct the analysis. The script must:

- Load and parse the input data (auto-detect filename in the data directory)
- Compute metrics suggested in section 1
- Generate the visualisations suggested in section 2
- Save visualisations to the current working directory
- Handle missing or empty data gracefully

## Success Criteria

✅ Suggested metrics are genuinely novel and insightful and will help guide future symposia
✅ Script runs without errors on the provided input data  
✅ Visualisations are properly labelled (titles, axis labels, legends)   
✅ Code is clean and minimal (no unnecessary utilities or visualisations)  
