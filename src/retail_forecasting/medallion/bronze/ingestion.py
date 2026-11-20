
"""Funciones de ingestión de datos en la capa Bronze."""

from pathlib import Path

from pyspark.sql import DataFrame, SparkSession


def read_raw_csv(
    spark: SparkSession,
    file_path: str | Path,
) -> DataFrame:
    """Leer un archivo CSV sin aplicar reglas de negocio."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"No existe el archivo: {path}"
        )

    return (
        spark.read
        .option("header", "true")
        .option("inferSchema", "false")
        .csv(str(path.resolve()))
    )


def write_bronze_parquet(
    df: DataFrame,
    output_path: str | Path,
    mode: str = "errorifexists",
) -> None:
    """Guardar un DataFrame Bronze en formato Parquet."""

    valid_modes = {
        "overwrite",
        "append",
        "ignore",
        "errorifexists",
    }

    if mode not in valid_modes:
        raise ValueError(
            f"Modo de escritura no válido: {mode}"
        )

    path = Path(output_path)

    (
        df.write
        .mode(mode)
        .parquet(str(path.resolve()))
    )
