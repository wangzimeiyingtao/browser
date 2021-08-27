from typing import Optional


class Error(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        self.name: Optional[str] = None
        self.stack: Optional[str] = None
        super().__init__(message)
