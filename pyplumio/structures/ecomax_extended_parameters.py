"""Contains an ecoMAX extended parameters structure decoder."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any, Final

from pyplumio.parameters import ParameterValues, unpack_parameter
from pyplumio.structures import StructureDecoder

ATTR_ECOMAX_EXTENDED_PARAMETERS: Final = "ecomax_extended_parameters"

ECOMAX_EXTENDED_PARAMETER_SIZE: Final = 3


class EcomaxExtendedParametersStructure(StructureDecoder):
    """Represents an ecoMAX extended parameters structure.

    Starts with number of parameters and index of the first parameter,
    followed by value, minimum value and maximum value of each
    parameter, one byte each.
    """

    __slots__ = ()

    def _ecomax_extended_parameter(
        self, message: bytes, start: int, count: int
    ) -> Generator[tuple[int, ParameterValues]]:
        """Unpack an ecoMAX extended parameter."""
        for index in range(start, start + count):
            if parameter := unpack_parameter(message, self._offset):
                yield (index, parameter)

            self._offset += ECOMAX_EXTENDED_PARAMETER_SIZE

    def decode(self, message: bytes, data: dict[str, Any], offset: int = 0) -> None:
        """Decode bytes and return message data and offset."""
        count = message[offset]
        start = message[offset + 1]
        self._offset = offset + 2
        count = min(
            count, (len(message) - self._offset) // ECOMAX_EXTENDED_PARAMETER_SIZE
        )
        data[ATTR_ECOMAX_EXTENDED_PARAMETERS] = list(
            self._ecomax_extended_parameter(message, start, count)
        )


__all__ = ["ATTR_ECOMAX_EXTENDED_PARAMETERS", "EcomaxExtendedParametersStructure"]
