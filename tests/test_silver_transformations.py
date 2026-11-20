
"""Pruebas de transformaciones Silver."""

from collections.abc import Iterator
from datetime import date

import pytest
from pyspark.sql import SparkSession

from retail_forecasting.medallion.silver.transformations import (
    cast_train_columns,
    select_forecasting_series,
)


@pytest.fixture(scope="module")
def spark() -> Iterator[SparkSession]:
    """Crear una sesión Spark para las pruebas."""
    session = (
        SparkSession.builder
        .master("local[2]")
        .appName("SilverTransformationsTests")
        .getOrCreate()
    )
    session.sparkContext.setLogLevel("ERROR")

    yield session

    session.stop()


def test_cast_train_columns(spark: SparkSession) -> None:
    """Verificar la conversión de tipos."""

    df = spark.createDataFrame(
        [
            ("1", "2016-12-30", "3", "DAIRY", "100.5", "2"),
        ],
        [
            "id",
            "date",
            "store_nbr",
            "family",
            "sales",
            "onpromotion",
        ],
    )

    result = cast_train_columns(df)
    row = result.first()

    assert row is not None
    assert result.schema["id"].dataType.simpleString() == "bigint"
    assert result.schema["date"].dataType.simpleString() == "date"
    assert result.schema["sales"].dataType.simpleString() == "double"
    assert row["date"] == date(2016, 12, 30)
    assert row["sales"] == 100.5


def test_select_forecasting_series(spark: SparkSession) -> None:
    """Verificar filtros de tienda, familia y fecha."""

    df = spark.createDataFrame(
        [
            (3, "DAIRY", date(2016, 12, 30)),
            (11, "MEATS", date(2016, 12, 31)),
            (99, "DAIRY", date(2016, 12, 30)),
            (3, "BOOKS", date(2016, 12, 30)),
            (3, "DAIRY", date(2017, 1, 1)),
        ],
        ["store_nbr", "family", "date"],
    )

    result = select_forecasting_series(
        df=df,
        stores=(3, 11),
        families=("DAIRY", "MEATS"),
        cutoff_date=date(2016, 12, 31),
    )

    assert result.count() == 2


def test_select_forecasting_series_sin_tiendas(
    spark: SparkSession,
) -> None:
    """Rechazar una selección de tiendas vacía."""

    df = spark.createDataFrame(
        [(3, "DAIRY", date(2016, 12, 30))],
        ["store_nbr", "family", "date"],
    )

    with pytest.raises(ValueError, match="tiendas está vacía"):
        select_forecasting_series(
            df=df,
            stores=(),
            families=("DAIRY",),
            cutoff_date=date(2016, 12, 31),
        )


def test_select_forecasting_series_sin_familias(
    spark: SparkSession,
) -> None:
    """Rechazar una selección de familias vacía."""

    df = spark.createDataFrame(
        [(3, "DAIRY", date(2016, 12, 30))],
        ["store_nbr", "family", "date"],
    )

    with pytest.raises(ValueError, match="familias está vacía"):
        select_forecasting_series(
            df=df,
            stores=(3,),
            families=(),
            cutoff_date=date(2016, 12, 31),
        )
