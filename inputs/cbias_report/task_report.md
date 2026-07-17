# Symposium Attendee Analysis - Exploratory Task

## Objective

Analyse data consisting of a series of CSV, XLSX, and TXT files, describing lists of attendees, abstract submissions,
and attendee feedback for a series of symposia. The aim is to explore the data and answer key questions about
year-to-year trends. Generate metrics and visualisations that provide insight and would be informative to key
stakeholders, such as the organising committee, life scientists, industry partners, funders, developer of bioimage
analysis software, and other stakeholders.

## Input

A parent directory, containing sub-directories for lists of registered attendees (Attendees), attendee feedback
(Feedback) and abstract submissions (Abstracts). Each sub-directory contains data for four years (2022-2025 inclusive):

- **Attendees**: one CSV per year (`CBIAS_<year>_Attendees.csv`), one row per registration, including a ticket
  type/category (e.g. Academic, Industry, Online Only, Sponsors).
- **Feedback**: one XLSX per year (Microsoft Forms export), one row per respondent, columns are the survey
  questions asked that year.
- **Abstracts**: one sub-folder per year (`<year>_Abstracts`), each containing one plain-text file per submission
  (`<n>_Abstract.txt`) with `Label: value` fields (title, authors, abstract text, keywords, etc.).

Note: file formats, column names, and field labels are not perfectly consistent across all four years - handle
missing/renamed fields gracefully rather than assuming an identical schema every year.

## Guiding Questions for Analysis

Your analysis should help answer these exploratory questions:

1. **Trends**: Are there any trends in the data that can help us understand the evolution of the symposia over time?
2. **Industry Participation**: What is the distribution of industry participation across the symposia?
3. **Attendee Demographics**: What is the distribution of attendee demographics across the symposia? Does this differ by year?
4. **Abstract Content**: Does the language used in abstract submissions change over time? If so, how?
5. **Feedback**: Do common themes emerge in attendee feedback? Are these constant over time or changing?

## Analysis Requirements

### 1. Suggest Key metrics
Analyse the input data and suggest **at least five key metrics** that help answer the guiding questions above. Choose
metrics that are:
- Computable from the available data
- Relevant to at least one of the guiding questions
- More insightful than just raw counts (consider timing, distribution, and patterns)
- Time-series or trend plots if timing data is available
- Heatmaps to show patterns across dimensions
- Scatter plots to show data distribution and variability
- Cumulative time-series to display how patterns or distributions have shifted over time
- Prioritise plots that show all data (e.g. scatter) over those that summarise (bar, pie)
- The visualisations of these metrics (see next section) must be inspired by plot examples in the MatplotLib and Seaborn galleries, so these examples should inform your choice of metrics:
  - https://github.com/matplotlib/matplotlib/tree/main/galleries
  - https://github.com/mwaskom/seaborn/tree/master/examples

### 2. Create Visualisations (PNG files)
Create **at least five visualisations** that illustrate the metrics chosen in section 1. Pick visualisations that help
answer the guiding questions:
- Time-series or trend plots
- Heatmaps to show patterns across dimensions
- Scatter plots to show data distribution and variability
- Chosen plots should closely match one of the plot examples in the MatplotLib and Seaborn galleries:
  - https://github.com/matplotlib/matplotlib/tree/main/galleries
  - https://github.com/mwaskom/seaborn/tree/master/examples

### 3. Identify Data Gaps

After analysis, print **at least three specific suggestions** for additional data/fields that would improve future analysis:
- Focus on what data would help answer the guiding questions more clearly
- Format: Bulleted list with a brief explanation of why each would be useful

## Output Requirements

The script must:
- Load and parse the input data (auto-detect filename in the data directory)
- Compute metrics suggested in section 1
- Print metrics to the console in a readable tabular format
- Generate the visualisations suggested in section 2
- Print data gap analysis suggestions to the console
- Save visualisations to the current working directory with specified filenames
- Handle missing or empty data gracefully

## Success Criteria

✅ Script runs without errors on the provided input data  
✅ At least five metrics are computed and printed  
✅ At least five PNG visualisation files are created and saved  
✅ Visualisations are properly labelled (titles, axis labels, legends)   
✅ Code is clean and minimal (no unnecessary utilities or visualisations)  
✅ One-line docstrings for all functions  
