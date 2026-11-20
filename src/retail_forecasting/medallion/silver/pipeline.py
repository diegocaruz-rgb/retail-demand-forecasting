
"""Pipeline de procesamiento de la capa Silver."""

import argparse
from pathlib import Path

from retail_forecasting.config.settings import (
    SELECTED_FAMILIES,
    SELECTED_STORES,
    SELECTION_CUTOFF,
)
from retail_forecasting.config.spark_session import create_spark_session
from retail_forecasting.medallion.silver.quality import validate_train_data
from retail_forecasting.medallion.silver.transformations import (
    cast_train_columns,
    select_forecasting_series,
)


def run_silver_pipeline(
    source_path: Path,
    destination_path: Path,
) -> None:
    """Transformar, validar y almacenar datos Silver."""

    spark = create_spark_session(
        app_name="RetailForecastingSilver"
    )

    try:
        print(f"Origen: {source_path}")
        print(f"Destino: {destination_path}")

        # 1. Leer datos Bronze
        df_bronze = spark.read.parquet(
            str(source_path.resolve())
        )

        # 2. Convertir tipos
        df_silver = cast_train_columns(df_bronze)

        # 3. Validar calidad
        validate_train_data(df_silver)
        print("Calidad de datos validada")

        # 4. Seleccionar series de forecasting
        df_selected = select_forecasting_series(
            df=df_silver,
            stores=SELECTED_STORES,
            families=SELECTED_FAMILIES,
            cutoff_date=SELECTION_CUTOFF,
        )

        # 5. Guardar en formato Parquet
        df_selected.write.mode("errorifexists").parquet(
            str(destination_path.resolve())
        )

        print("Pipeline Silver completado correctamente")

    finally:
        spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ejecutar pipeline Silver"
    )

    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Directorio Parquet de Bronze",
    )

    parser.add_argument(
        "--destination",
        type=Path,
        required=True,
        help="Directorio Parquet de Silver",
    )

    args = parser.parse_args()

    run_silver_pipeline(
        source_path=args.source,
        destination_path=args.destination,
    )
