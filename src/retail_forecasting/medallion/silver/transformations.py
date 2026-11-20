
"""Transformaciones de datos de la capa Silver."""

from datetime import date

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def cast_train_columns(df: DataFrame) -> DataFrame:
    """Convertir columnas de entrenamiento a sus tipos esperados."""

    required_columns = {
        "id",
        "date",
        "store_nbr",
        "family",
        "sales",
        "onpromotion",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Columnas faltantes: {sorted(missing_columns)}"
        )

    return df.select(
        F.col("id").cast("long").alias("id"),
        F.to_date(F.col("date"), "yyyy-MM-dd").alias("date"),
        F.col("store_nbr").cast("integer").alias("store_nbr"),
        F.col("family").cast("string").alias("family"),
        F.col("sales").cast("double").alias("sales"),
        F.col("onpromotion").cast("integer").alias("onpromotion"),
    )


def select_forecasting_series(
    df: DataFrame,
    stores: tuple[int, ...],
    families: tuple[str, ...],
    cutoff_date: date,
) -> DataFrame:
    """Seleccionar tiendas, familias y fechas para forecasting."""

    if not stores:
        raise ValueError("La selección de tiendas está vacía")

    if not families:
        raise ValueError("La selección de familias está vacía")

    return df.filter(
        F.col("store_nbr").isin(*stores)
        & F.col("family").isin(*families)
        & (F.col("date") <= F.lit(cutoff_date))
    )
