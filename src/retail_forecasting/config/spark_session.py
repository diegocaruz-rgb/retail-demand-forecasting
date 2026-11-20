
"""Configuración de sesiones locales de Apache Spark."""

from pyspark.sql import SparkSession


def create_spark_session(
    app_name: str = "RetailForecasting",
    master: str = "local[2]",
    driver_memory: str = "2g",
    shuffle_partitions: int = 4,
) -> SparkSession:
    """Crear o reutilizar una sesión Spark configurada."""

    if not app_name.strip():
        raise ValueError("app_name no puede estar vacío")

    if shuffle_partitions < 1:
        raise ValueError(
            "shuffle_partitions debe ser mayor que cero"
        )

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.driver.memory", driver_memory)
        .config(
            "spark.sql.shuffle.partitions",
            str(shuffle_partitions),
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark
