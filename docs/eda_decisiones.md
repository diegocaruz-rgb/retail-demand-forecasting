
# Decisiones del análisis exploratorio

## 1. Dataset

Fuente: Kaggle Store Sales - Time Series Forecasting.

Datos principales:
- 54 tiendas.
- 33 familias de productos.
- 1,782 combinaciones tienda-familia.
- Datos de entrenamiento: 2013-01-01 a 2017-08-15.
- Horizonte de predicción: 16 días.

## 2. Corte temporal de selección

Fecha límite: 2016-12-31.

Las tiendas y familias se seleccionaron utilizando
únicamente información disponible hasta esta fecha.

Los datos posteriores se reservaron para evaluación.

## 3. Selección de tiendas

Se seleccionó una tienda por tipo comercial (A-E).

Criterios:
- Al menos 365 días con ventas positivas.
- Prioridad por días con ventas positivas.
- Desempate por ventas diarias promedio.
- Desempate final por identificador de tienda.

Tiendas seleccionadas: 3, 11, 28, 40, 44.

## 4. Selección de familias

Se buscaron distintos perfiles de demanda:
- Alta: 4 familias.
- Media: 3 familias.
- Baja: 3 familias.

Familias definitivas:
- AUTOMOTIVE
- BEVERAGES
- CELEBRATION
- DAIRY
- LIQUOR,WINE,BEER
- MAGAZINES
- MEATS
- PET SUPPLIES
- PREPARED FOODS
- PRODUCE

BOOKS y LADIESWEAR fueron sustituidas porque
presentaban combinaciones sin ventas históricas.

## 5. Validaciones

Resultados:
- 50 series seleccionadas.
- 72,850 registros históricos hasta el corte.
- 1,457 registros por serie.
- 50 series con ventas positivas.
- Mínimo de 370 días con ventas por serie.

No se detectaron valores nulos ni ventas negativas
en los datos originales de entrenamiento.

## 6. Consideraciones

- Existen cuatro fechas globales ausentes:
  25 de diciembre de 2013, 2014, 2015 y 2016.
- Algunas series tienen demanda intermitente.
- La selección no garantiza ventas futuras positivas.
- La selección es inicial y podrá ampliarse
  a las 1,782 series del dataset.

## 7. Reproducibilidad

La configuración está centralizada en:

src/retail_forecasting/config/settings.py

Las pruebas se encuentran en:

tests/test_settings.py

El análisis exploratorio está en:

notebooks/01_exploracion_datos.ipynb
