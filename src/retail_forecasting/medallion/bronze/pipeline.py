
"""Pipeline de ingestión de la capa Bronze."""

from pathlib import Path

from retail_forecasting.config.spark_session import (
    create_spark_session,
)
from retail_forecasting.medallion.bronze.ingestion import (
    read_raw_csv,
    write_bronze_parquet,
)


def run_bronze_pipeline(
    source_path: Path,
    destination_path: Path,
) -> None:
    """Leer un CSV y almacenarlo en Bronze como Parquet."""

    spark = create_spark_session(
        app_name="RetailForecastingBronze"
    )

    try:
        print(f"Origen: {source_path}")
        print(f"Destino: {destination_path}")

        df = read_raw_csv(spark, source_path)

        write_bronze_parquet(
            df=df,
            output_path=destination_path,
        )

        print("Ingestión Bronze completada")

    finally:
        spark.stop()



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Ejecutar ingestión Bronze"
    )

    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Ruta del CSV de origen",
    )

    parser.add_argument(
        "--destination",
        type=Path,
        required=True,
        help="Directorio Parquet de destino",
    )

    args = parser.parse_args()

    run_bronze_pipeline(
        source_path=args.source,
        destination_path=args.destination,
    )

