from pydantic import Field
from pydantic_settings import BaseSettings

from doc_scribe.domain.enums import ModelName


class Settings(BaseSettings):
    model_name: ModelName = ModelName.CLAUDE_3_5_SONNET
    """LLM name."""

    temperature: float = Field(default=0.1, ge=0.0, le=1.0)
    """Temperature controls the randomness of language model output. A high temperature produces
    more unpredictable and creative results, while a low temperature produces more deterministic
    and conservative output.
    """

    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    """Top-p filters out tokens whose cumulative probability is less than the specified threshold.
    It allows for more diversity in the output while still avoiding low-probability tokens."""

    max_tokens: int = Field(default=1_000_000, ge=0)
    """Maximum number of tokens that the LLM generates."""

    max_file_count: int = 100
    """Limit of files for generating the file level code analysis.
    If the project contains more files than this, we will simply use the module level analysis
    as documentation source for the high level documentation.
    """

    aws_default_region: str = "eu-central-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_session_token: str = ""
