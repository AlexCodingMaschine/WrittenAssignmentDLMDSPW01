"""Custom exceptions for the pipeline.
We can define specific exceptions for different error scenarios, instead of
a generic exception. This helps with precise error handling. And can be more clear"""

#Often just the name says it all!
class PipelineError(Exception):
    """Base exception for all pipeline errors."""
    pass


class DataLoadError(PipelineError):
    """Raised when data loading fails (DB read, CSV read)."""
    pass


class SelectionError(PipelineError):
    """Raised when ideal selection fails."""
    pass


class MatchingError(PipelineError):
    """Raised when test point matching fails."""
    pass


class ValidationError(PipelineError):
    """Raised when data validation fails (missing columns, bad types)."""
    pass
