"""Thin wrapper to load decision data."""
from decision_engine.data import (
    get_frontend_options,
    get_backend_options,
    get_database_options,
    get_all_options,
)

__all__ = [
    "get_frontend_options",
    "get_backend_options",
    "get_database_options",
    "get_all_options",
]
