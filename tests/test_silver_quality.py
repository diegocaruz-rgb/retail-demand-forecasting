"""Pruebas de calidad de datos de la capa Silver."""
from collections.abc import Iterator
from datetime import date

import pytest
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import (
    DateType,
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

from retail_forecasting.medallion.silver.quality import (
    validate_train_data,
)


@pytest.fixture(scope="module")
def spark() -> Iterator[SparkSession]:
    """Crear una sesión Spark compartida entre pruebas."""
    session = (
        SparkSession.builder
        .master("local[2]")
        .appName("SilverQualityTests")
        .getOrCreate()
    )
    session.sparkContext.setLogLevel("ERROR")

    yield session

    session.stop()



def crear_datos(
    spark: SparkSession,
    filas: list[
        tuple[int, date, int, str, float | None, int]
    ],
) -> DataFrame:
    """Crear datos de prueba con esquema explícito."""

    schema = StructType(
        [
            StructField("id", LongType(), True),
            StructField("date", DateType(), True),
            StructField("store_nbr", IntegerType(), True),
            StructField("family", StringType(), True),
            StructField("sales", DoubleType(), True),
            StructField("onpromotion", IntegerType(), True),
        ]
    )

    return spark.createDataFrame(
        filas,
        schema=schema,
    )



def test_datos_validos(spark: SparkSession) -> None:
    df = crear_datos(
        spark,
        [
            (1, date(2017, 1, 1), 3, "DAIRY", 100.0, 2),
            (2, date(2017, 1, 2), 3, "DAIRY", 120.0, 0),
        ],
    )

    validate_train_data(df)


def test_ventas_negativas(spark: SparkSession) -> None:
    df = crear_datos(
        spark,
        [(1, date(2017, 1, 1), 3, "DAIRY", -10.0, 0)],
    )

    with pytest.raises(ValueError, match="ventas inválidas"):
        validate_train_data(df)


def test_promociones_negativas(spark: SparkSession) -> None:
    df = crear_datos(
        spark,
        [(1, date(2017, 1, 1), 3, "DAIRY", 10.0, -1)],
    )

    with pytest.raises(ValueError, match="promociones negativas"):
        validate_train_data(df)


def test_duplicados(spark: SparkSession) -> None:
    df = crear_datos(
        spark,
        [
            (1, date(2017, 1, 1), 3, "DAIRY", 100.0, 0),
            (2, date(2017, 1, 1), 3, "DAIRY", 120.0, 0),
        ],
    )

    with pytest.raises(ValueError, match="duplicados"):
        validate_train_data(df)


def test_nulos(spark: SparkSession) -> None:
    df = crear_datos(
        spark,
        [(1, date(2017, 1, 1), 3, "DAIRY", None, 0)],
    )

    with pytest.raises(ValueError, match="valores nulos"):
        validate_train_data(df)
