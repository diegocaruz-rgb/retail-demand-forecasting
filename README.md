# Retail Demand Forecasting Platform

End-to-end retail demand forecasting platform built with Python, PySpark, XGBoost, FastAPI and MLOps practices.

## Project Overview

This project aims to build a production-oriented machine learning platform for forecasting daily retail sales using the Kaggle Store Sales dataset.

The platform will cover data ingestion, data engineering, feature engineering, model training, evaluation, batch prediction, API serving and cloud deployment.

## Business Objective

Forecast daily unit sales for the next **16 days** at the store and product-family level.

Initial scope:
- 5 stores
- 10 product families
- 50 time series
- Up to 800 daily predictions per forecasting run

## Technology Stack

- **Language:** Python 3.12
- **Data Engineering:** PySpark, SQL, Medallion Architecture
- **Machine Learning:** XGBoost
- **Experiment Tracking:** MLflow
- **API:** FastAPI, Pydantic
- **Orchestration:** Apache Airflow
- **Cloud:** Google Cloud Platform
- **Quality:** pytest, Ruff, mypy
- **DevOps:** Git, GitHub Actions, Docker

## Forecasting Strategy

- Seasonal naive baseline
- Global XGBoost forecasting model
- Lag, rolling-window, calendar and promotion features
- Expanding-window backtesting
- Independent final test set
- Primary evaluation metric: RMSLE
- Secondary metrics: WAPE and MAE

## Architecture

The platform will follow a modular architecture with Bronze, Silver and Gold data layers.

Forecasts will be generated in batch and exposed through an API.

## Project Status

**In development — Day 1**

Completed:
- Python environment configuration
- Modular project structure
- Editable Python package installation
- Ruff, pytest and mypy configuration
- First business validation function and automated tests
- Git repository initialization and GitHub publication

## Dataset

Kaggle: Store Sales — Time Series Forecasting

https://www.kaggle.com/competitions/store-sales-time-series-forecasting

Raw datasets and generated artifacts are excluded from Git version control.

## Roadmap

Target duration: 20 development days, with up to 5 additional days if necessary.

1. Project setup and software engineering foundations
2. Data ingestion and Medallion architecture
3. Feature engineering and forecasting models
4. Model evaluation and experiment tracking
5. API development and containerization
6. Workflow orchestration and cloud integration
7. CI/CD, testing, documentation and final demonstration

## License

No license has been selected yet.
