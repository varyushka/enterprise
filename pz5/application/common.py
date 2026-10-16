from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

class ErrorCode(Enum):
    NOT_FOUND = 'NOT_FOUND'
    VALIDATION_ERROR = 'VALIDATION_ERROR'

@dataclass(frozen=True)
class Error:
    code: ErrorCode
    message: str

@dataclass(frozen=True)
class Result:
    value: Any = None
    error: Optional[Error] = None

    @property
    def is_success(self) -> bool:
        return self.error is None

    @classmethod
    def success(cls, value: Any):
        return cls(value=value)

    @classmethod
    def failure(cls, error: Error):
        return cls(error=error)