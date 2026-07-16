"""Crick Bioimage Analysis Symposium (CBIAS) domain configuration for the pipeline.

Analyses four years (2022-2025) of attendee registrations, post-event feedback surveys, and abstract
submissions to answer year-on-year trend questions (see inputs/cbias_report/task_report.md).

NOTE: `docker_image` below does not exist yet. This repo's Dockerfile only builds `bia-analysis:latest`
(numpy/scipy/scikit-image/scikit-learn/pandas/bioio/bioio-tifffile - no matplotlib, no openpyxl). Build
a `cbias-analysis:latest` image with pandas, numpy, matplotlib, and openpyxl (needed for the .xlsx
feedback files) before execution-validation will work for this config - same gap already documented for
`trello_config.py`'s `python-analysis:latest`.
"""

import re
from pathlib import Path

import pandas as pd

from config import PipelineConfig

AVAILABLE_LIBRARIES = """
Available libraries for imports:
- Standard library: os, sys, re, csv, json, pathlib, datetime, collections, string
- NumPy: for numerical computing
- Pandas: for data manipulation and analysis (pandas.read_excel works - openpyxl is installed)
- Matplotlib: for plotting and visualization
"""

DOMAIN_NOTES = """
Analyse four years (2022-2025) of CBIAS data, in three sub-directories under the data directory (or
INPUT_FOLDER env var):

- Attendees/CBIAS_<year>_Attendees.csv - one row per registration. Columns drift slightly by year:
  2022-2024 use "Attendee Surname" / "Purchaser town/city" / "Purchaser county"; 2025 renames these to
  "Attendee last name" / "Purchaser city" / "Purchaser state". Read each file's own header rather than
  assuming one fixed schema across years.
  IMPORTANT: 3 of the 4 CSVs are NOT valid UTF-8 (they contain Latin-1 bytes from accented characters in
  names/towns) - try encoding="utf-8" and fall back to encoding="latin-1" on UnicodeDecodeError; never
  assume plain UTF-8 will work for all four files.
  "Ticket type" holds the registration category: Academic, Academic - early bird, Industry,
  Industry - early bird, Online Only, Sponsors. Treat "X" and "X - early bird" as the same category X
  (e.g. match on a substring/prefix) when computing category distributions; "Industry" plus
  "Industry - early bird" together are the industry-participation signal.

- Feedback/CBIAS <year> Attendee Survey(...).xlsx - one row per respondent, one file per year. This is a
  raw Microsoft Forms export: each survey question appears as a real answer column plus two
  auto-generated companion columns ("Points - <question>", "Feedback - <question>") that are
  quiz-scoring artifacts and almost always empty - ignore columns starting with "Points - " or
  "Feedback - " and read the plain question-text column for actual responses. Question wording drifts
  slightly by year for the same underlying construct - e.g. "The ticket prices were appropriate"
  (2022-2023) becomes "The ticket prices were too high" (2024-2025), an inverted phrasing of the same
  question - match columns by keyword substring (e.g. "ticket price"), not exact text, and account for
  the polarity flip when combining years into one trend. Likert-style answers are free-text strings
  (e.g. "Strongly agree"), not numbers - map them to an ordinal scale before averaging.

- Abstracts/<year>_Abstracts/<n>_Abstract.txt - one plain-text file per submission, "Label: value"
  lines. The field set differs by year: 2022-2023 files have Name/Email/Institution/Title/Authors/
  Affiliation/Abstract/Keywords/Additional Keywords; 2024-2025 files drop "Name" and "Affiliation" and
  add "Themes" and "Gender of presenting author" (2025 sometimes also has "Special requirements"). Parse
  leniently by known field-label prefixes rather than assuming a fixed field order or a complete set per
  file - a few files also have one-off extra fields (e.g. "References", "Presenting author"). The
  "Keywords" / "Additional Keywords" value is a Python-list-literal string (e.g.
  ["Segmentation","Object Tracking"]) with occasional stray "\\n" inside entries - strip whitespace after
  parsing.
"""

_ABSTRACT_FIELD_LABELS = [
    "Name", "Email", "Institution", "Title", "Authors", "Affiliation", "Affiliations",
    "Abstract", "Keywords", "Additional Keywords", "Themes", "Gender of presenting author",
    "Special requirements", "References", "Presenting author", "doi",
]
_ABSTRACT_FIELD_PATTERN = re.compile(
    r"^(" + "|".join(re.escape(label) for label in _ABSTRACT_FIELD_LABELS) + r"):", re.MULTILINE
)

# Microsoft Forms export columns that are metadata, not survey questions - dropped when
# summarizing "question_columns" below so the orchestrator sees the real questions, not response IDs.
_FEEDBACK_METADATA_COLUMNS = {
    "id", "start time", "completion time", "email", "name", "total points",
    "quiz feedback", "last modified time",
}


def _read_attendees_csv(path: Path) -> pd.DataFrame:
    """Read an attendee CSV, falling back to latin-1 since 3 of the 4 years aren't valid UTF-8."""
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")


def _feedback_question_columns(columns: list[str]) -> list[str]:
    """Real survey-question columns: drop ID/timestamp metadata and the auto-generated
    'Points - '/'Feedback - ' companion columns Microsoft Forms adds per question."""
    return [
        c for c in columns
        if c.strip().lower() not in _FEEDBACK_METADATA_COLUMNS
        and not c.startswith("Points - ")
        and not c.startswith("Feedback - ")
    ]


def extract_input_metadata(directory: str) -> str:
    """Summarize the Attendees/Feedback/Abstracts sub-directories for the orchestrator."""
    base = Path(directory)

    attendees = []
    for f in sorted(base.glob("Attendees/*.csv")):
        df = _read_attendees_csv(f)
        ticket_counts = df["Ticket type"].value_counts(dropna=False) if "Ticket type" in df.columns else {}
        attendees.append({
            "file": f.name,
            "rows": len(df),
            "columns": list(df.columns),
            "ticket_type_counts": {str(k): int(v) for k, v in ticket_counts.items()},
        })

    feedback = []
    for f in sorted(base.glob("Feedback/*.xlsx")):
        df = pd.read_excel(f)
        feedback.append({
            "file": f.name,
            "respondents": len(df),
            "question_columns": _feedback_question_columns(list(df.columns)),
        })

    abstracts = []
    for year_dir in sorted(base.glob("Abstracts/*_Abstracts")):
        files = sorted(year_dir.glob("*_Abstract.txt"))
        fields_seen = set()
        for f in files:
            fields_seen.update(_ABSTRACT_FIELD_PATTERN.findall(f.read_text(encoding="utf-8")))
        abstracts.append({
            "folder": year_dir.name,
            "submissions": len(files),
            "fields_present": sorted(fields_seen),
        })

    return str({"Attendees": attendees, "Feedback": feedback, "Abstracts": abstracts})


CONFIG = PipelineConfig(
    orchestrator_model="claude-opus-4-8",
    worker_model="claude-sonnet-5",
    compiler_model="claude-opus-4-8",
    requirements_evaluator_model="claude-sonnet-5",
    docker_image="cbias-analysis:latest",
    available_libraries=AVAILABLE_LIBRARIES,
    domain_notes=DOMAIN_NOTES,
    extract_input_metadata=extract_input_metadata,
)