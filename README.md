# Multi-Agent Code Generation Pipeline

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.14+](https://img.shields.io/badge/Python-3.14+-green.svg)](https://www.python.org/downloads/)
[![Claude API](https://img.shields.io/badge/Claude-API-orange.svg)](https://www.anthropic.com)
[![Docker](https://img.shields.io/badge/Docker-containerized-blue.svg)](https://www.docker.com)

A reusable template for generating, validating, and optimizing Python scripts using a multi-agent orchestration pattern. Given a task description and input data, it uses Claude to design an architecture, implement it in parallel, assemble it, and iteratively refine it until the generated code passes validation.

## How It Works

```
Task Report + Input Data
        ↓
Orchestrator (architecture design)
        ↓
Workers (parallel implementation)
        ↓
Compiler (assemble into one script)
        ↓
Evaluator (Docker execution + validation)
        ↓
  Pass → Final Script
  Fail → Feedback loop back to Orchestrator
```

- **Role-based models**: Opus 4.8 (architecture), Sonnet 5 (compilation/evaluation), Haiku 4.5 (implementation) — matched to task complexity. Swap in `config.py` for different tasks.
- **Containerized execution**: Generated scripts run in a pre-built Docker image with pinned dependencies, ensuring code only uses pre-installed libraries.
- **Structured I/O**: XML-tagged prompts/responses for reliable parsing and validation.

## Adapting to a New Domain

The pipeline is agnostic to the problem domain. To retarget it for a different application:

1. **Create a domain config** (e.g., `my_domain_config.py`):
   - Subclass or create a `PipelineConfig` (see `config.py` for the interface)
   - Define `available_libraries` (the list of allowed imports for the generated script)
   - Define `domain_notes` (any domain-specific constraints for the LLM)
   - Provide an `extract_input_metadata(data_dir)` function that scans input files and returns a description
   - Specify the Docker image name and models to use

2. **Update `app.py`**:
   - Change the import from `bioimage_config` to your new config file

3. **Update `Dockerfile`** (if using different libraries):
   - Pre-install your domain's required packages

4. **Update `pixi.toml`** (optional):
   - Add your domain's Python dependencies

See `bioimage_config.py` for a concrete example.

## Example: Bioimage Analysis

This template ships with a working bioimage analysis example. To use it:

### Setup

Requirements: Python 3.14+, Docker Desktop running, an Anthropic API key.

```bash
pip install -r requirements.txt
docker build -t bia-analysis:latest .
export ANTHROPIC_API_KEY="your-key-here"
```

### Usage

Place a task report and sample TIFF images under `inputs/`:

```
inputs/report/report_YYYYMMDD_HHMMSS.md
inputs/images/*.tif
```

Then run:

```bash
python app.py
```

The final validated script is written to `outputs/analysis_script_<timestamp>.py`.

### Notes

- Generated scripts are restricted to pre-installed libraries (numpy, scipy, scikit-image, scikit-learn, pandas, bioio, bioio-tifffile, and standard library)
- Execution timeout: 300s; max 5 redesign iterations (both configurable via `--max-iterations` and code)
- Docker is required to validate execution — without it, evaluation skips the run step and checks code quality only

## License

GPL-3.0 - See [LICENSE](LICENSE) for details.
