
"""Pruebas del módulo de configuración de Spark."""

import pytest
from pyspark.sql import SparkSession

from retail_forecasting.config.spark_session import (
    create_spark_session,
)


def test_app_name_vacio() -> None:
    """Rechazar nombres de aplicación vacíos."""
    with pytest.raises(ValueError):
        create_spark_session(app_name="   ")


def test_shuffle_partitions_invalido() -> None:
    """Rechazar particiones menores que uno."""
    with pytest.raises(ValueError):
        create_spark_session(shuffle_partitions=0)


def test_create_spark_session() -> None:
    """Comprobar la creación de una sesión Spark local."""
    spark: SparkSession = create_spark_session(
        app_name="RetailForecastingTest",
        master="local[2]",
        driver_memory="2g",
        shuffle_partitions=4,
    )

    try:
        assert spark.sparkContext.master == "local[2]"
        assert spark.sparkContext.appName == "RetailForecastingTest"
        assert (
            spark.conf.get("spark.sql.shuffle.partitions")
            == "4"
        )

        datos = [(1, "BEVERAGES", 150.0)]
        df = spark.createDataFrame(
            datos,
            ["store_nbr", "family", "sales"],
        )

        assert df.count() == 1

    finally:
        spark.stop()
