"""Shared request helpers for BRO XML request modules.

This module centralizes:
- Required/optional kwargs validation.
- Optional kwargs normalization.
- Lightweight typing support for `srcdocdata` payloads.
- Dataclass-friendly conversion for source document payload input.
"""

from collections.abc import Mapping
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any


@dataclass(frozen=True)
class SourceDocData:
    """Typed wrapper for source-document payloads.

    Parameters
    ----------
    data:
        The source document payload as a mapping.
    """

    data: Mapping[str, Any]


def has_value(value: Any) -> bool:
    """Return True when a value should be treated as present.

    Empty strings and `None` are treated as missing values.
    """

    if value is None:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    return True


def normalize_optional_kwargs(
    kwargs: dict[str, Any], optional_keys: list[str] | tuple[str, ...]
) -> None:
    """Remove optional kwargs that are present but effectively empty."""

    for key in optional_keys:
        if key in kwargs and not has_value(kwargs[key]):
            del kwargs[key]


def check_required_kwargs(
    kwargs: Mapping[str, Any], constraints: Mapping[str, str], method: str
) -> None:
    """Validate that all obligated keys have non-empty values."""

    missing_or_empty = []
    for key, requirement in constraints.items():
        if requirement == "obligated" and not has_value(kwargs.get(key)):
            missing_or_empty.append(key)

    if missing_or_empty:
        raise Exception(
            "Obligated input arguments missing or empty for '{}': {}".format(
                method, "".join(str(e) + " " for e in missing_or_empty)
            )
        )


def coerce_srcdocdata(value: Any) -> dict[str, Any]:
    """Convert srcdocdata input to a plain dictionary.

    Supported input types:
    - `dict` / mapping
    - `SourceDocData`
    - Any dataclass instance (converted via `dataclasses.asdict`)
    """

    if isinstance(value, SourceDocData):
        return dict(value.data)

    if isinstance(value, Mapping):
        return dict(value)

    if is_dataclass(value) and not isinstance(value, type):
        converted = asdict(value)
        if not isinstance(converted, dict):
            raise TypeError("Dataclass srcdocdata could not be converted to a dict")
        return converted

    raise TypeError(
        "Unsupported srcdocdata type. Use dict, SourceDocData, or a dataclass instance."
    )


def coerce_mapping_like(value: Any, context: str) -> dict[str, Any]:
    """Coerce a mapping-like/dataclass object to a dictionary."""

    try:
        return coerce_srcdocdata(value)
    except TypeError as exc:
        raise TypeError(f"{context} must be dict-like or dataclass-convertible") from exc


def coerce_list_of_mapping_like(values: Any, context: str) -> list[dict[str, Any]]:
    """Coerce a list of mapping-like/dataclass objects to dictionaries."""

    if not isinstance(values, list):
        raise TypeError(f"{context} must be a list")

    return [coerce_mapping_like(value, f"{context}[{index}]") for index, value in enumerate(values)]
