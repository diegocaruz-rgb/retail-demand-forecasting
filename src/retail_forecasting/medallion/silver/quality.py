
"""Validaciones de calidad de datos de la capa Silver."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def validate_train_data(df: DataFrame) -> None:
    """Validar reglas básicas de calidad del dataset train."""

    required_columns = [
        "id",
        "date",
        "store_nbr",
        "family",
        "sales",
        "onpromotion",
    ]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Columnas faltantes: {sorted(missing_columns)}"
        )

    # Validar nulos en columnas obligatorias
    null_condition = None

    for column in required_columns:
        condition = F.col(column).isNull()
        null_condition = (
            condition
            if null_condition is None
            else null_condition | condition
        )

    if null_condition is not None and df.filter(
        null_condition
    ).limit(1).count() > 0:
        raise ValueError("Se encontraron valores nulos")

    # Validar ventas negativas o NaN
    if df.filter(
        (F.col("sales") < 0)
        | F.isnan("sales")
    ).limit(1).count() > 0:
        raise ValueError("Se encontraron ventas inválidas")

    # Validar promociones negativas
    if df.filter(
        F.col("onpromotion") < 0
    ).limit(1).count() > 0:
        raise ValueError("Se encontraron promociones negativas")

    # Validar duplicados por clave de negocio
    duplicates = (
        df.groupBy("date", "store_nbr", "family")
        .count()
        .filter(F.col("count") > 1)
    )

    if duplicates.limit(1).count() > 0:
        raise ValueError(
            "Se encontraron duplicados por fecha, tienda y familia"
        )
