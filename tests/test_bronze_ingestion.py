
"""Pruebas de lectura y escritura de la capa Bronze."""

from pathlib import Path

import pytest

from retail_forecasting.config.spark_session import (
    create_spark_session,
)
from retail_forecasting.medallion.bronze.ingestion import (
    read_raw_csv,
    write_bronze_parquet,
)


def test_read_raw_csv(tmp_path: Path) -> None:
    """Leer CSV y conservar sus columnas como texto."""
    csv_path = tmp_path / "sample.csv"

    csv_path.write_text(
        "store_nbr,family,sales\n"
        "3,BEVERAGES,150.0\n"
        "11,DAIRY,85.0\n",
        encoding="utf-8",
    )

    spark = create_spark_session(
        app_name="TestBronzeRead"
    )

    try:
        df = read_raw_csv(spark, csv_path)

        assert df.count() == 2
        assert df.columns == [
            "store_nbr",
            "family",
            "sales",
        ]
        assert all(
            field.dataType.simpleString() == "string"
            for field in df.schema.fields
        )

    finally:
        spark.stop()


def test_read_raw_csv_inexistente(
    tmp_path: Path,
) -> None:
    """Rechazar archivos que no existen."""
    spark = create_spark_session(
        app_name="TestBronzeMissing"
    )

    try:
        with pytest.raises(FileNotFoundError):
            read_raw_csv(
                spark,
                tmp_path / "missing.csv",
            )
    finally:
        spark.stop()


def test_write_bronze_parquet(
    tmp_path: Path,
) -> None:
    """Guardar y recuperar datos en Parquet."""
    spark = create_spark_session(
        app_name="TestBronzeWrite"
    )

    try:
        df = spark.createDataFrame(
            [
                ("3", "BEVERAGES", "150.0"),
                ("11", "DAIRY", "85.0"),
            ],
            ["store_nbr", "family", "sales"],
        )

        output_path = tmp_path / "bronze"

        write_bronze_parquet(df, output_path)

        df_recuperado = spark.read.parquet(
            str(output_path)
        )

        assert df_recuperado.count() == 2
        assert df_recuperado.schema == df.schema

    finally:
        spark.stop()


def test_write_mode_invalido(
    tmp_path: Path,
) -> None:
    """Rechazar modos de escritura desconocidos."""
    spark = create_spark_session(
        app_name="TestBronzeMode"
    )

    try:
        df = spark.createDataFrame(
            [("3",)],
            ["store_nbr"],
        )

        with pytest.raises(ValueError):
            write_bronze_parquet(
                df,
                tmp_path / "bronze",
                mode="invalid",
            )
    finally:
        spark.stop()
