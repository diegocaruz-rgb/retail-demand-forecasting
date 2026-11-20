
"""Pruebas de configuración del proyecto."""

from datetime import date

from retail_forecasting.config.settings import (
    EXPECTED_SERIES,
    FORECAST_HORIZON,
    SELECTED_FAMILIES,
    SELECTED_STORES,
    SELECTION_CUTOFF,
)


def test_forecast_horizon() -> None:
    """El horizonte de predicción debe ser de 16 días."""
    assert FORECAST_HORIZON == 16


def test_selection_cutoff() -> None:
    """La selección utiliza datos hasta diciembre de 2016."""
    assert SELECTION_CUTOFF == date(2016, 12, 31)


def test_selected_stores() -> None:
    """Deben existir cinco tiendas únicas."""
    assert len(SELECTED_STORES) == 5
    assert len(set(SELECTED_STORES)) == 5


def test_selected_families() -> None:
    """Deben existir diez familias únicas."""
    assert len(SELECTED_FAMILIES) == 10
    assert len(set(SELECTED_FAMILIES)) == 10


def test_expected_series() -> None:
    """La configuración debe producir exactamente 50 series."""
    assert EXPECTED_SERIES == 50
    assert EXPECTED_SERIES == (
        len(SELECTED_STORES) * len(SELECTED_FAMILIES)
    )
