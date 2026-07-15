from dataclasses import dataclass, field
from typing import Callable

# Default per-design stances: cycled across the parallel designs in an iteration (design m gets
# stance m % len(design_stances)) so they explore different regions of the solution space without
# any extra LLM calls - just a different one-line steer in each orchestrator prompt.
DEFAULT_DESIGN_STANCES = [
    "Conventional & robust - take the most direct, straightforward approach that reliably satisfies the criteria.",
    "Depth-first - pick the single most important question or requirement and answer it far more thoroughly than the rest; keep everything else minimal.",
    "Contrarian - name one assumption a conventional approach here would rely on, then design an approach that doesn't depend on it.",
]


@dataclass
class PipelineConfig:
    """Configuration for the multi-agent code-generation pipeline.

    This is the swap point for adapting the pipeline to a new domain.
    Create a new config file (e.g. bioimage_config.py) and pass an instance
    of PipelineConfig to generate_and_optimize().
    """
    orchestrator_model: str
    worker_model: str
    compiler_model: str
    requirements_evaluator_model: str
    docker_image: str
    available_libraries: str
    domain_notes: str
    extract_input_metadata: Callable[[str], str]
    design_stances: list[str] = field(default_factory=lambda: list(DEFAULT_DESIGN_STANCES))
