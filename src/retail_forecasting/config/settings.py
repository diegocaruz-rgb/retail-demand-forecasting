
"""Configuración inicial de la plataforma de forecasting."""

from datetime import date

# Horizonte de predicción
FORECAST_HORIZON = 16

# Corte utilizado para seleccionar las series
SELECTION_CUTOFF = date(2016, 12, 31)

# Tiendas seleccionadas
SELECTED_STORES: tuple[int, ...] = (
    3,
    11,
    28,
    40,
    44,
)

# Familias seleccionadas
SELECTED_FAMILIES: tuple[str, ...] = (
    "AUTOMOTIVE",
    "BEVERAGES",
    "CELEBRATION",
    "DAIRY",
    "LIQUOR,WINE,BEER",
    "MAGAZINES",
    "MEATS",
    "PET SUPPLIES",
    "PREPARED FOODS",
    "PRODUCE",
)

# Número esperado de series
EXPECTED_SERIES = (
    len(SELECTED_STORES) * len(SELECTED_FAMILIES)
)
