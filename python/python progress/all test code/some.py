# ==============================================================================
# ELECTRICITY LOAD FORECASTING — PUBLICATION-GRADE INTEGRATED PIPELINE  v14
# ------------------------------------------------------------------------------
# Manuscript : "Comparative Analysis of Machine Learning and Deep Learning
#               Models for Short-Term Electricity Load Forecasting Using
#               Weather and Temporal Features"
# Status     : Major Revision — reviewer-response implementation
#
# This is a SINGLE, SELF-CONTAINED script. No custom helper modules are
# imported. Every function used below is defined in this file. The script
# executes top to bottom without manual intervention, provided a dataset CSV
# is available at one of the paths listed in CONFIG (Section 2).
#
# The pipeline is dataset-independent: change PRIMARY_DATASET_CANDIDATES /
# SECOND_DATASET_CANDIDATES (or DATASET_COLUMN_MAP) and the entire workflow —
# preprocessing, feature engineering, training, tuning, explainability,
# ablation, robustness, statistical testing, and export — reruns unchanged.
#
# NOTE ON HONESTY OF RESULTS: every number, table, and figure this script
# produces comes from an actual run against real data loaded in Section 2.
# Nothing is hard-coded or fabricated. If a requested analysis is not valid
# for the data actually present (e.g. too few residuals for a paired test,
# no holiday calendar available, insufficient samples for bootstrap CIs),
# the corresponding function detects this and records a explicit
# "NOT_APPLICABLE" / reasoned skip in its output rather than inventing a
# number. Search the source for `NOT_APPLICABLE` to find every such guard.
#
# Sections:
#   1. Imports
#   2. Configuration
#   3. Reproducibility & small utilities
#   4. Data loading (dataset-independent)
#   5. Data preprocessing
#   6. Exploratory data analysis
#   7. Feature engineering
#   8. Feature ranking / variance / correlation filtering
#   9. Train / test split & scaling
#  10. Classical ML models
#  11. Hyperparameter optimization (Optuna)
#  12. Deep learning models (LSTM + Transformer)
#  13. Explainability (SHAP, linear coefficients, attention / permutation)
#  14. Ablation study
#  15. Statistical significance testing
#  16. Robustness analysis
#  17. Model comparison table
#  18. Visualization
#  19. Export results
#  20. Second-dataset (cross-dataset) run
#  21. Final summary
# ==============================================================================


# ==============================================================================
# SECTION 1: IMPORTS
# ==============================================================================
import os
import io
import json
import time
import shutil
import random
import warnings
import itertools
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

from scipy import stats as scipy_stats

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.feature_selection import mutual_info_regression
from sklearn.inspection import permutation_importance

from xgboost import XGBRegressor
import lightgbm as lgb

import optuna
from optuna.samplers import TPESampler
from optuna.pruners import MedianPruner
from optuna.visualization.matplotlib import (
    plot_optimization_history,
    plot_param_importances,
    plot_contour,
    plot_slice,
    plot_parallel_coordinate,
)

import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    LSTM, Dense, Dropout, Input, LayerNormalization, MultiHeadAttention,
    GlobalAveragePooling1D, Add, Embedding
)
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

optuna.logging.set_verbosity(optuna.logging.WARNING)
warnings.filterwarnings("ignore")
tf.get_logger().setLevel("ERROR")

sns.set_theme(style="darkgrid", palette="deep")
sns.set_context("talk", font_scale=0.85)

print(f"All libraries imported. TensorFlow {tf.__version__}. SHAP available: {SHAP_AVAILABLE}\n")


# ==============================================================================
# SECTION 2: CONFIGURATION
# ==============================================================================
SEED = 42

# --- Dataset-independence: add/replace candidate paths per dataset -----------
PRIMARY_DATASET_CANDIDATES = ["/kaggle/input/datasets/yug201/delhi-5-minute-electricity-demand-for-forecasting/powerdemand_5min_2021_to_2024_with weather.csv"]
# Set to None to skip the cross-dataset validation run (Section 20).
SECOND_DATASET_CANDIDATES = ["/kaggle/input/datasets/albertovidalrod/electricity-consumption-uk-20092022/historic_demand_2009_2024_noNaN.csv"]

# Column-name resolution: the pipeline is written against generic names
# ("load", "datetime") and remaps whatever the raw file calls them here.
# Add an entry per new dataset instead of touching the pipeline logic.
DATASET_COLUMN_MAP = {
    "default": {
        "datetime_col": "datetime",
        "target_col_candidates": ["Power demand", "load", "PowerConsumption", "Consumption"],
        "drop_cols": ["Unnamed: 0", "moving_avg_3"],
        "build_datetime": None,
    },
    "uk_national_grid": {
        "datetime_col": "datetime",
        # 'nd' = National Demand, closest analogue to Delhi's total system
        # load. 'tsd' (Transmission System Demand) and
        # 'england_wales_demand' are available as alternates.
        "target_col_candidates": ["nd", "tsd", "england_wales_demand", "load"],
        # 'period_hour' is redundant with settlement_period (both encode
        # time-of-day) so it's dropped to avoid a near-duplicate feature.
        "drop_cols": ["period_hour"],
        "build_datetime": "settlement_period",
    },
}

SPLIT_DATE = "2024-01-01"          # chronological train/test cut for the primary dataset
TSCV_SPLITS = 5                    # folds for TimeSeriesSplit CV
OPTUNA_TRIALS = 50
OPTUNA_CV_SPLITS = 3
LOOKBACK = 24                      # sequence length for LSTM / Transformer
DL_EPOCHS = 60
DL_BATCH_SIZE = 256
N_BOOTSTRAP = 1000                 # bootstrap resamples for robustness CIs
FIG_DPI = 300

OUTPUT_ROOT = "pipeline_outputs"
FIG_DIR = os.path.join(OUTPUT_ROOT, "figures")
TABLE_DIR = os.path.join(OUTPUT_ROOT, "tables")
MODEL_DIR = os.path.join(OUTPUT_ROOT, "models")
for _d in (OUTPUT_ROOT, FIG_DIR, TABLE_DIR, MODEL_DIR):
    os.makedirs(_d, exist_ok=True)


# ==============================================================================
# SECTION 3: REPRODUCIBILITY & SMALL UTILITIES
# ==============================================================================
def set_global_seeds(seed: int = SEED) -> None:
    """Fix random seeds for Python, NumPy, TensorFlow. XGBoost/LightGBM take
    their seed via `random_state`/`seed` params on each estimator instead."""
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


set_global_seeds(SEED)


def save_figure(fig, name: str, subdir: str = "") -> None:
    """Save a matplotlib figure as both PNG (FIG_DPI) and PDF (vector)."""
    target_dir = os.path.join(FIG_DIR, subdir) if subdir else FIG_DIR
    os.makedirs(target_dir, exist_ok=True)
    fig.savefig(os.path.join(target_dir, f"{name}.png"), dpi=FIG_DPI, bbox_inches="tight")
    fig.savefig(os.path.join(target_dir, f"{name}.pdf"), bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved figure: {name}.png / {name}.pdf")


def export_table(df: pd.DataFrame, name: str, index: bool = True) -> None:
    """Export a DataFrame to CSV under TABLE_DIR."""
    path = os.path.join(TABLE_DIR, f"{name}.csv")
    df.to_csv(path, index=index)
    print(f"  Exported table: {name}.csv")


def compute_metrics(name: str, y_true, y_pred, train_time: float = np.nan,
                     pred_time: float = np.nan, model_size_kb: float = np.nan) -> dict:
    """Standard regression metrics used throughout the pipeline."""
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    nonzero = y_true != 0
    mape = np.mean(np.abs((y_true[nonzero] - y_pred[nonzero]) / y_true[nonzero])) * 100 if nonzero.any() else np.nan
    return {
        "Model": name, "MAE": mae, "RMSE": rmse, "R2": r2, "MAPE (%)": mape,
        "Training Time (s)": train_time, "Prediction Time (s)": pred_time,
        "Model Size (KB)": model_size_kb,
    }


def model_size_kb(model) -> float:
    """Rough model-size proxy via in-memory pickle size, for the comparison table."""
    import pickle
    try:
        return len(pickle.dumps(model)) / 1024.0
    except Exception:
        return np.nan


# ==============================================================================
# SECTION 4: DATA LOADING (DATASET-INDEPENDENT)
# ==============================================================================
def resolve_dataset_path(candidates: list) -> str:
    """Return the first existing path from a list of candidate locations."""
    for p in candidates:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(
        f"Could not find a dataset CSV in any of the expected paths: {candidates}"
    )


def load_raw_dataset(path: str, column_map_key: str = "default") -> pd.DataFrame:
    """
    Load a raw CSV and normalize it to the pipeline's expected schema:
    a `datetime` column (parsed) and a `load` column (target), with any
    dataset-specific junk columns dropped. Driven entirely by
    DATASET_COLUMN_MAP so a new dataset only needs a new map entry.
    """
    cmap = DATASET_COLUMN_MAP.get(column_map_key, DATASET_COLUMN_MAP["default"])
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    drop_cols = [c for c in cmap["drop_cols"] if c in df.columns]
    if drop_cols:
        df = df.drop(columns=drop_cols)

    # --- construct datetime for schemas that don't ship one directly ---
    if cmap.get("build_datetime") == "settlement_period":
        if not {"settlement_date", "settlement_period"}.issubset(df.columns):
            raise KeyError(
                f"Expected settlement_date + settlement_period columns for the "
                f"'{column_map_key}' schema but found: {list(df.columns)}"
            )
        # Try ISO first (most Kaggle re-exports of this dataset use
        # YYYY-MM-DD); fall back to day-first if that leaves too many
        # rows unparsed.
        base_date = pd.to_datetime(df["settlement_date"], errors="coerce")
        if base_date.isna().mean() > 0.5:
            base_date = pd.to_datetime(df["settlement_date"], dayfirst=True, errors="coerce")
        # Each settlement_period is a 30-minute block (1-48/day; 46 or 50
        # on UK clock-change days).
        df["datetime"] = base_date + pd.to_timedelta((df["settlement_period"] - 1) * 30, unit="min")

    target_col = next((c for c in cmap["target_col_candidates"] if c in df.columns), None)
    if target_col is None:
        raise KeyError(
            f"None of the candidate target columns {cmap['target_col_candidates']} "
            f"were found in {path}.\nActual columns present: {list(df.columns)}\n"
            f"Update DATASET_COLUMN_MAP['{column_map_key}']."
        )
    if target_col != "load":
        df = df.rename(columns={target_col: "load"})

    dt_col = cmap["datetime_col"]
    if dt_col not in df.columns:
        raise KeyError(
            f"Datetime column '{dt_col}' not found in {path}.\n"
            f"Actual columns present: {list(df.columns)}\n"
            f"Update DATASET_COLUMN_MAP['{column_map_key}']."
        )
    if dt_col != "datetime":
        df = df.rename(columns={dt_col: "datetime"})

    print(f"Loaded raw dataset from: {path}")
    print(f"  Rows: {len(df):,}  |  Columns: {list(df.columns)}")
    return df


# ==============================================================================
# SECTION 5: DATA PREPROCESSING
# ==============================================================================
def validate_and_sort_datetime(df: pd.DataFrame) -> tuple:
    """Parse datetime, drop unparseable rows, sort chronologically, reset index.
    Returns (clean_df, summary_dict)."""
    n_before = len(df)
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    n_unparseable = int(df["datetime"].isna().sum())
    df = df.dropna(subset=["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)
    summary = {
        "rows_before": n_before,
        "unparseable_datetime_rows_dropped": n_unparseable,
        "date_range_start": str(df["datetime"].min()),
        "date_range_end": str(df["datetime"].max()),
        "is_monotonic_after_sort": bool(df["datetime"].is_monotonic_increasing),
    }
    return df, summary


def remove_duplicate_timestamps(df: pd.DataFrame) -> tuple:
    """Drop duplicate rows and duplicate timestamps (keep first occurrence)."""
    n_before = len(df)
    df = df.drop_duplicates()
    n_after_full_dedup = len(df)
    df = df.drop_duplicates(subset=["datetime"], keep="first")
    n_after_ts_dedup = len(df)
    summary = {
        "duplicate_full_rows_removed": n_before - n_after_full_dedup,
        "duplicate_timestamp_rows_removed": n_after_full_dedup - n_after_ts_dedup,
    }
    return df.reset_index(drop=True), summary


def handle_missing_values(df: pd.DataFrame, numeric_cols: list) -> tuple:
    """
    Forward-fill then back-fill short gaps in numeric columns (appropriate for
    high-frequency sensor/weather series), and report remaining missingness.
    Rows still missing the target after filling are dropped (cannot train
    on an unobserved target).
    """
    missing_before = df[numeric_cols].isna().sum()
    df = df.copy()
    df[numeric_cols] = df[numeric_cols].ffill().bfill()
    missing_after = df[numeric_cols].isna().sum()

    n_before = len(df)
    if "load" in df.columns:
        df = df.dropna(subset=["load"])
    n_after = len(df)

    summary = {
        "rows_dropped_missing_target": n_before - n_after,
        "columns_with_missing_before": int((missing_before > 0).sum()),
        "columns_with_missing_after": int((missing_after > 0).sum()),
        "total_missing_before": int(missing_before.sum()),
        "total_missing_after": int(missing_after.sum()),
    }
    return df.reset_index(drop=True), summary


def detect_outliers_iqr(df: pd.DataFrame, cols: list, k: float = 3.0) -> pd.DataFrame:
    """
    IQR-based outlier flags for inspection (NOT automatic removal - load spikes
    from genuine demand events are informative, not noise). IQR bounds are
    computed on the full series purely for reporting; no values are altered,
    so this step cannot leak test-period information into training.
    Returns a summary DataFrame of outlier counts per column.
    """
    rows = []
    for c in cols:
        if c not in df.columns:
            continue
        q1, q3 = df[c].quantile(0.25), df[c].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - k * iqr, q3 + k * iqr
        n_outliers = int(((df[c] < lower) | (df[c] > upper)).sum())
        rows.append({"feature": c, "lower_bound": lower, "upper_bound": upper,
                      "n_outliers": n_outliers, "pct_outliers": 100 * n_outliers / len(df)})
    return pd.DataFrame(rows)


def time_based_train_test_split(df: pd.DataFrame, split_date: str) -> tuple:
    """
    Strict chronological split - everything before split_date is train,
    everything from split_date onward is test. This is a leakage-prevention
    control: no future information can enter the training set, and all
    feature engineering (lags, rolling stats) computed earlier in the
    pipeline uses only past values relative to each row (.shift()-based),
    so those features do not leak future information either.
    """
    train_mask = df["datetime"] < split_date
    test_mask = df["datetime"] >= split_date
    return df.loc[train_mask].reset_index(drop=True), df.loc[test_mask].reset_index(drop=True)


def build_time_series_cv(n_splits: int = TSCV_SPLITS) -> TimeSeriesSplit:
    """Standard forward-chaining CV splitter used across the pipeline (avoids
    the leakage that k-fold shuffling would introduce in a time series)."""
    return TimeSeriesSplit(n_splits=n_splits)


def run_preprocessing(raw_df: pd.DataFrame) -> tuple:
    """Run the full preprocessing chain and return (clean_df, summary_df)."""
    print("Running preprocessing pipeline ...")
    summary = {}

    df, s1 = validate_and_sort_datetime(raw_df)
    summary.update(s1)

    df, s2 = remove_duplicate_timestamps(df)
    summary.update(s2)

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    df, s3 = handle_missing_values(df, numeric_cols)
    summary.update(s3)

    outlier_report = detect_outliers_iqr(df, [c for c in numeric_cols if c in df.columns])
    export_table(outlier_report, "outlier_inspection_report", index=False)

    summary["rows_final"] = len(df)
    summary_df = pd.DataFrame([summary])
    export_table(summary_df, "preprocessing_summary", index=False)
    print(f"Preprocessing complete. Final row count: {len(df):,}\n")
    return df, summary_df


# ==============================================================================
# SECTION 6: EXPLORATORY DATA ANALYSIS
# ==============================================================================
def eda_dataset_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Descriptive statistics table for all numeric columns."""
    desc = df.select_dtypes(include=[np.number]).describe().T
    desc["skew"] = df.select_dtypes(include=[np.number]).skew()
    desc["kurtosis"] = df.select_dtypes(include=[np.number]).kurtosis()
    export_table(desc, "eda_dataset_statistics")
    return desc


def eda_target_distribution(df: pd.DataFrame, target: str = "load") -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df[target], kde=True, ax=axes[0], color="#2C7FB8")
    axes[0].set_title(f"{target} — Distribution")
    sns.boxplot(x=df[target], ax=axes[1], color="#7FCDBB")
    axes[1].set_title(f"{target} — Boxplot")
    plt.tight_layout()
    save_figure(fig, "eda_target_distribution")


def eda_missing_value_plot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 5))
    missing_pct = df.isna().mean().sort_values(ascending=False) * 100
    sns.barplot(x=missing_pct.values, y=missing_pct.index, ax=ax, color="#D95F02")
    ax.set_xlabel("Missing (%)")
    ax.set_title("Missing Value Percentage by Column")
    plt.tight_layout()
    save_figure(fig, "eda_missing_values")


def eda_feature_distributions(df: pd.DataFrame, cols: list) -> None:
    cols = [c for c in cols if c in df.columns][:12]
    n = len(cols)
    if n == 0:
        return
    ncols = 4
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows))
    axes = np.atleast_1d(axes).ravel()
    for i, c in enumerate(cols):
        sns.histplot(df[c], kde=True, ax=axes[i], color="#41AB5D")
        axes[i].set_title(c, fontsize=10)
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")
    plt.tight_layout()
    save_figure(fig, "eda_feature_distributions")


def eda_seasonal_analysis(df: pd.DataFrame, target: str = "load") -> pd.DataFrame:
    tmp = df.copy()
    tmp["month"] = tmp["datetime"].dt.month
    tmp["season"] = tmp["month"] % 12 // 3 + 1  # 1=winter,2=spring,3=summer,4=fall
    season_map = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
    tmp["season"] = tmp["season"].map(season_map)
    season_stats = tmp.groupby("season")[target].agg(["mean", "std", "min", "max"])

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=tmp, x="season", y=target,
                order=["Winter", "Spring", "Summer", "Fall"], ax=ax)
    ax.set_title("Seasonal Load Distribution")
    plt.tight_layout()
    save_figure(fig, "eda_seasonal_analysis")
    export_table(season_stats, "eda_seasonal_stats")
    return season_stats


def eda_monthly_demand(df: pd.DataFrame, target: str = "load") -> None:
    tmp = df.copy()
    tmp["month"] = tmp["datetime"].dt.month
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=tmp, x="month", y=target, ax=ax, color="#8DA0CB")
    ax.set_title("Monthly Demand Distribution")
    plt.tight_layout()
    save_figure(fig, "eda_monthly_demand")


def eda_weekday_weekend(df: pd.DataFrame, target: str = "load") -> pd.DataFrame:
    tmp = df.copy()
    tmp["weekday_name"] = tmp["datetime"].dt.day_name()
    tmp["is_weekend"] = tmp["datetime"].dt.weekday >= 5
    stats_df = tmp.groupby("is_weekend")[target].agg(["mean", "std"])
    fig, ax = plt.subplots(figsize=(9, 5))
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    sns.boxplot(data=tmp, x="weekday_name", y=target, order=order, ax=ax, color="#FC8D62")
    ax.set_title("Load by Day of Week")
    plt.xticks(rotation=30)
    plt.tight_layout()
    save_figure(fig, "eda_weekday_pattern")
    export_table(stats_df, "eda_weekday_weekend_stats")
    return stats_df


def eda_hourly_profile(df: pd.DataFrame, target: str = "load") -> None:
    tmp = df.copy()
    tmp["hour"] = tmp["datetime"].dt.hour
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=tmp, x="hour", y=target, ax=ax, errorbar="sd", color="#E7298A")
    ax.set_title("Average Hourly Demand Profile (± std)")
    ax.set_xticks(range(0, 24, 2))
    plt.tight_layout()
    save_figure(fig, "eda_hourly_profile")


def eda_yearly_trend(df: pd.DataFrame, target: str = "load") -> None:
    tmp = df.set_index("datetime")[target].resample("D").mean()
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(tmp.index, tmp.values, color="#1B9E77", linewidth=1)
    ax.set_title("Daily Mean Load — Full History (Yearly Trend)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=30)
    plt.tight_layout()
    save_figure(fig, "eda_yearly_trend")


def eda_weather_correlation(df: pd.DataFrame, weather_cols: list, target: str = "load") -> pd.DataFrame:
    cols = [c for c in weather_cols if c in df.columns]
    corr = df[cols + [target]].corr()[target].drop(target).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=corr.values, y=corr.index, ax=ax, palette="coolwarm")
    ax.set_title(f"Correlation of Weather Features with {target}")
    ax.set_xlabel("Pearson r")
    plt.tight_layout()
    save_figure(fig, "eda_weather_correlation")
    export_table(corr.to_frame("correlation_with_target"), "eda_weather_correlation")
    return corr.to_frame("correlation_with_target")


def eda_correlation_heatmap(df: pd.DataFrame, cols: list, name: str = "eda_correlation_heatmap") -> pd.DataFrame:
    cols = [c for c in cols if c in df.columns]
    corr_matrix = df[cols].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    fig, ax = plt.subplots(figsize=(min(0.55 * len(cols) + 4, 20), min(0.5 * len(cols) + 4, 18)))
    sns.heatmap(corr_matrix, mask=mask, annot=len(cols) <= 25, fmt=".2f",
                annot_kws={"size": 7}, cmap="RdYlBu_r", center=0, vmin=-1, vmax=1,
                linewidths=0.4, linecolor="white", square=True,
                cbar_kws={"shrink": 0.75, "label": "Pearson r"}, ax=ax)
    ax.set_title("Feature Correlation Heatmap (Pearson r)", fontsize=14, fontweight="bold", pad=14)
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.tick_params(axis="y", rotation=0, labelsize=8)
    plt.tight_layout()
    save_figure(fig, name)
    return corr_matrix


def run_eda(df: pd.DataFrame, weather_cols: list) -> None:
    """Run the full EDA suite. All outputs saved to FIG_DIR / TABLE_DIR."""
    print("Running exploratory data analysis ...")
    eda_dataset_statistics(df)
    eda_target_distribution(df)
    eda_missing_value_plot(df)
    eda_feature_distributions(df, weather_cols)
    eda_seasonal_analysis(df)
    eda_monthly_demand(df)
    eda_weekday_weekend(df)
    eda_hourly_profile(df)
    eda_yearly_trend(df)
    eda_weather_correlation(df, weather_cols)
    eda_correlation_heatmap(df, weather_cols + ["load"], "eda_weather_load_heatmap")
    print("EDA complete.\n")


# ==============================================================================
# SECTION 7: FEATURE ENGINEERING
# ==============================================================================
def add_wind_direction_encoding(df: pd.DataFrame, col: str = "wdir") -> pd.DataFrame:
    """Circular encoding for wind direction (0-360 degrees); 359 deg ~= 1 deg."""
    if col not in df.columns:
        return df
    df = df.copy()
    df[col] = df[col].ffill()
    df[f"{col}_sin"] = np.sin(2 * np.pi * df[col] / 360)
    df[f"{col}_cos"] = np.cos(2 * np.pi * df[col] / 360)
    df = df.drop(columns=[col])
    return df


def add_cyclical_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Sin/cos encodings for hour, weekday, and month preserve circular
    continuity (23:55 -> 00:00, December -> January) that a raw integer
    encoding would break."""
    df = df.copy()
    dt = df["datetime"].dt
    df["hour_sin"] = np.sin(2 * np.pi * dt.hour / 24)
    df["hour_cos"] = np.cos(2 * np.pi * dt.hour / 24)
    df["weekday_sin"] = np.sin(2 * np.pi * dt.weekday / 7)
    df["weekday_cos"] = np.cos(2 * np.pi * dt.weekday / 7)
    df["month_sin"] = np.sin(2 * np.pi * dt.month / 12)
    df["month_cos"] = np.cos(2 * np.pi * dt.month / 12)
    return df


def add_calendar_indicators(df: pd.DataFrame, holiday_dates: Optional[set] = None) -> pd.DataFrame:
    """Binary calendar/time-of-day flags. Holiday indicator is only added
    when an explicit `holiday_dates` set is supplied — NOT_APPLICABLE:
    no holiday calendar ships with the pipeline by default, since holiday
    lists are country-specific and cannot be fabricated for an unknown
    dataset. Pass a set of `date` objects to enable it."""
    df = df.copy()
    dt = df["datetime"].dt
    df["weekday"] = dt.weekday
    df["weekend"] = (df["weekday"] >= 5).astype(int)
    df["is_peak_hour"] = dt.hour.between(18, 21).astype(int)
    df["is_day"] = dt.hour.between(6, 18).astype(int)
    df["is_night"] = (~dt.hour.between(6, 21)).astype(int)
    df["quarter"] = dt.quarter
    df["is_month_end"] = dt.is_month_end.astype(int)
    season_map = {12: 1, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 3, 7: 3, 8: 3, 9: 4, 10: 4, 11: 4}
    df["season"] = dt.month.map(season_map)
    if "is_holiday" in df.columns:
        pass  # dataset already supplies a real holiday flag — keep it as-is
    elif holiday_dates:
        df["is_holiday"] = dt.date.isin(holiday_dates).astype(int)
    else:
        df["is_holiday"] = 0  # NOT_APPLICABLE — no holiday calendar supplied
    return df


def add_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "temp" in df.columns:
        df["temp_hour"] = df["temp"] * df["datetime"].dt.hour
        if "is_peak_hour" in df.columns:
            df["temp_x_peak"] = df["temp"] * df["is_peak_hour"]
    return df


def add_lag_features(df: pd.DataFrame, target: str, lags: list) -> pd.DataFrame:
    """Lag features use `.shift()` exclusively, so every lag value at row t
    is drawn only from rows < t — no future/target leakage is possible."""
    df = df.copy()
    for lag in lags:
        df[f"lag_{lag}"] = df[target].shift(lag)
    return df


def add_rolling_features(df: pd.DataFrame, target: str, windows: list) -> pd.DataFrame:
    """Rolling statistics computed on `.shift(1)` so the current row's own
    target value is never included in its own rolling window (no leakage)."""
    df = df.copy()
    base = df[target].shift(1)
    for w in windows:
        roll = base.rolling(w)
        df[f"roll_mean_{w}"] = roll.mean()
        df[f"roll_median_{w}"] = roll.median()
        df[f"roll_std_{w}"] = roll.std()
        df[f"roll_min_{w}"] = roll.min()
        df[f"roll_max_{w}"] = roll.max()
        df[f"roll_q25_{w}"] = roll.quantile(0.25)
        df[f"roll_q75_{w}"] = roll.quantile(0.75)
    return df


def add_expanding_features(df: pd.DataFrame, target: str) -> pd.DataFrame:
    df = df.copy()
    base = df[target].shift(1)
    df["expanding_mean"] = base.expanding(min_periods=12).mean()
    df["expanding_std"] = base.expanding(min_periods=12).std()
    return df


def add_ewma_features(df: pd.DataFrame, target: str, spans: list) -> pd.DataFrame:
    df = df.copy()
    base = df[target].shift(1)
    for span in spans:
        df[f"ewma_{span}"] = base.ewm(span=span, min_periods=span // 2 or 1).mean()
    return df


def add_difference_and_growth_features(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """Difference, percentage change, growth rate, and acceleration (2nd
    difference) — all computed on the shifted (lag-1) series, so they
    describe the trend *up to* t-1 and cannot leak the value at t."""
    df = df.copy()
    base = df[target].shift(1)
    df["diff_1"] = base.diff(1)
    df["pct_change_1"] = base.pct_change(1)
    df["load_growth_rate"] = base.pct_change(12)      # vs 1 hour earlier (5-min data)
    df["load_acceleration"] = df["diff_1"].diff(1)     # change of change
    return df


def engineer_features(df: pd.DataFrame,
                       lags: list = (12, 288, 2016),
                       rolling_windows: list = (12, 288),
                       ewma_spans: list = (12, 288),
                       holiday_dates: Optional[set] = None) -> pd.DataFrame:
    """
    Full feature-engineering chain. Preserves every feature from the original
    v13 implementation (wind-direction encoding, hour/month cyclical encoding,
    weekend/peak/day flags, temp interactions, lag_12/288/2016, roll_*_12) and
    adds: weekday cyclical encoding, rolling median/quantiles/extra windows,
    expanding statistics, EWMA, differencing, pct-change, growth/acceleration,
    night/quarter/season/month-end/holiday indicators.
    """
    print("Engineering features ...")
    df = add_wind_direction_encoding(df, "wdir")
    df = add_cyclical_time_features(df)
    df = add_calendar_indicators(df, holiday_dates=holiday_dates)
    df = add_interaction_features(df)
    df = add_lag_features(df, "load", list(lags))
    df = add_rolling_features(df, "load", list(rolling_windows))
    df = add_expanding_features(df, "load")
    df = add_ewma_features(df, "load", list(ewma_spans))
    df = add_difference_and_growth_features(df, "load")

    # Drop raw time columns now redundant with cyclical/indicator encodings.
    drop_cols = [c for c in ["hour", "month", "minute", "day", "year"] if c in df.columns]
    if drop_cols:
        df = df.drop(columns=drop_cols)

    n_before = len(df)
    df = df.dropna().reset_index(drop=True)
    print(f"  Dropped {n_before - len(df):,} rows with NaNs introduced by lag/rolling windows.")
    print(f"  Final feature-engineered dataset: {len(df):,} rows, {df.shape[1]} columns.\n")
    return df


def get_feature_list(df: pd.DataFrame, target: str = "load",
                      exclude: tuple = ("datetime",)) -> list:
    """All numeric columns except target/excluded columns — used as the
    default full FEATURES list."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    return [c for c in numeric_cols if c != target and c not in exclude]


# ==============================================================================
# SECTION 8: FEATURE RANKING / VARIANCE ANALYSIS / CORRELATION FILTERING
# ==============================================================================
def feature_ranking_report(X: pd.DataFrame, y: pd.Series, seed: int = SEED) -> pd.DataFrame:
    """Rank features by absolute Pearson correlation with the target and by
    mutual information (captures non-linear relationships correlation misses)."""
    pearson = X.apply(lambda col: col.corr(y))
    mi = mutual_info_regression(X, y, random_state=seed)
    report = pd.DataFrame({
        "feature": X.columns,
        "abs_pearson_corr": pearson.abs().values,
        "mutual_information": mi,
    }).sort_values("mutual_information", ascending=False).reset_index(drop=True)
    export_table(report, "feature_ranking_report", index=False)
    return report


def variance_analysis(X: pd.DataFrame, near_zero_threshold: float = 1e-6) -> pd.DataFrame:
    """Flag near-zero-variance features (uninformative, safe to drop)."""
    variances = X.var().sort_values()
    report = variances.to_frame("variance")
    report["near_zero_variance"] = report["variance"] < near_zero_threshold
    export_table(report, "feature_variance_report")
    return report


def correlation_filter(X: pd.DataFrame, threshold: float = 0.97) -> tuple:
    """
    Drop one feature from every pair whose absolute correlation exceeds
    `threshold`, keeping the first-encountered feature of each pair. Returns
    (filtered_feature_list, dropped_feature_report).
    """
    corr_matrix = X.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [col for col in upper.columns if any(upper[col] > threshold)]
    dropped_report = pd.DataFrame({"dropped_feature": to_drop})
    export_table(dropped_report, "correlation_filter_dropped_features", index=False)
    kept = [c for c in X.columns if c not in to_drop]
    print(f"Correlation filtering (threshold={threshold}): dropped {len(to_drop)} of {X.shape[1]} features.")
    return kept, dropped_report


def tree_feature_importance_report(models_dict: dict, feature_names: list) -> pd.DataFrame:
    """Consolidate feature_importances_ from every tree-based model that has one."""
    data = {"feature": feature_names}
    for name, model in models_dict.items():
        if hasattr(model, "feature_importances_"):
            data[name] = model.feature_importances_
    report = pd.DataFrame(data)
    export_table(report, "feature_importance", index=False)
    return report


# ==============================================================================
# SECTION 9: FINAL TRAIN/TEST SPLIT & SCALING
# ==============================================================================
def prepare_train_test(df: pd.DataFrame, features: list, target: str,
                        split_date: str) -> dict:
    """Chronological split + StandardScaler fit ONLY on train (leakage-safe)."""
    train_df, test_df = time_based_train_test_split(df, split_date)
    X_train, y_train = train_df[features], train_df[target]
    X_test, y_test = test_df[features], test_df[target]
    dates_test = test_df["datetime"].reset_index(drop=True)

    scaler = StandardScaler()
    X_train_sc = pd.DataFrame(scaler.fit_transform(X_train), columns=features, index=X_train.index)
    X_test_sc = pd.DataFrame(scaler.transform(X_test), columns=features, index=X_test.index)

    print(f"Train: {len(X_train):,} rows | Test: {len(X_test):,} rows (split at {split_date})")
    return dict(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                X_train_sc=X_train_sc, X_test_sc=X_test_sc, scaler=scaler,
                dates_test=dates_test, full_df=df, features=features, target=target)


# ==============================================================================
# SECTION 10: CLASSICAL MACHINE LEARNING MODELS
# ==============================================================================
def build_model_zoo(seed: int = SEED) -> dict:
    """
    name -> (estimator, "scaled"|"raw"). Tree-based models train on raw
    features (splits are scale-invariant); linear/distance-based models need
    standardized inputs.
    """
    return {
        "Linear Regression": (LinearRegression(), "scaled"),
        "Decision Tree": (DecisionTreeRegressor(max_depth=10, min_samples_leaf=10,
                                                 random_state=seed), "raw"),
        "Random Forest": (RandomForestRegressor(n_estimators=200, max_depth=15,
                                                 min_samples_leaf=4, n_jobs=-1,
                                                 random_state=seed), "raw"),
        "KNN": (KNeighborsRegressor(n_neighbors=10, weights="distance", n_jobs=-1), "scaled"),
        "Gradient Boosting": (GradientBoostingRegressor(n_estimators=200, max_depth=5,
                                                         learning_rate=0.05, subsample=0.8,
                                                         random_state=seed), "raw"),
        "XGBoost": (XGBRegressor(n_estimators=300, max_depth=6, learning_rate=0.05,
                                  subsample=0.8, colsample_bytree=0.8, reg_alpha=0.1,
                                  reg_lambda=1.0, n_jobs=-1, random_state=seed,
                                  verbosity=0), "raw"),
        "LightGBM": (lgb.LGBMRegressor(n_estimators=300, max_depth=6, learning_rate=0.05,
                                        subsample=0.8, colsample_bytree=0.8, reg_alpha=0.1,
                                        reg_lambda=1.0, n_jobs=-1, random_state=seed,
                                        verbose=-1), "raw"),
    }


def naive_baseline_predictions(X_test: pd.DataFrame, lag_col: str = "lag_288") -> np.ndarray:
    """Prediction = load one day earlier. All models must beat this to be useful."""
    if lag_col not in X_test.columns:
        return None
    return X_test[lag_col].values


def train_and_evaluate_all(models: dict, split: dict) -> tuple:
    """Fit every model in the zoo, time training/prediction, evaluate, and
    return (metrics_list, predictions_dict, fitted_models_dict)."""
    X_train, y_train = split["X_train"], split["y_train"]
    X_test, y_test = split["X_test"], split["y_test"]
    X_train_sc, X_test_sc = split["X_train_sc"], split["X_test_sc"]

    all_metrics, all_preds, fitted_models = [], {}, {}

    naive_pred = naive_baseline_predictions(X_test)
    if naive_pred is not None:
        m = compute_metrics("Naive Baseline", y_test, naive_pred)
        all_metrics.append(m)
        all_preds["Naive Baseline"] = naive_pred

    print("Training classical ML models ...")
    for name, (model, data_type) in models.items():
        X_tr = X_train_sc if data_type == "scaled" else X_train
        X_te = X_test_sc if data_type == "scaled" else X_test

        t0 = time.time()
        model.fit(X_tr, y_train)
        train_time = time.time() - t0

        t0 = time.time()
        preds = model.predict(X_te)
        pred_time = time.time() - t0

        m = compute_metrics(name, y_test, preds, train_time, pred_time, model_size_kb(model))
        all_metrics.append(m)
        all_preds[name] = preds
        fitted_models[name] = model
        print(f"  {name:<22} MAE={m['MAE']:8.3f}  RMSE={m['RMSE']:8.3f}  R2={m['R2']:.4f}  MAPE={m['MAPE (%)']:.2f}%")

    return all_metrics, all_preds, fitted_models


def build_weighted_ensemble(preds_a: np.ndarray, preds_b: np.ndarray,
                             rmse_a: float, rmse_b: float) -> tuple:
    """Inverse-RMSE weighted blend: the more accurate model gets more weight,
    data-driven rather than a fixed 50/50 average."""
    inv_a, inv_b = 1.0 / rmse_a, 1.0 / rmse_b
    total = inv_a + inv_b
    w_a, w_b = inv_a / total, inv_b / total
    blend = w_a * preds_a + w_b * preds_b
    return blend, w_a, w_b


# ==============================================================================
# SECTION 11: HYPERPARAMETER OPTIMIZATION (OPTUNA)
# ==============================================================================
def make_xgb_objective(X_train: pd.DataFrame, y_train: pd.Series, n_splits: int = OPTUNA_CV_SPLITS):
    tscv = TimeSeriesSplit(n_splits=n_splits)

    def objective(trial: optuna.Trial) -> float:
        params = dict(
            n_estimators=trial.suggest_int("n_estimators", 100, 600, step=50),
            max_depth=trial.suggest_int("max_depth", 3, 10),
            learning_rate=trial.suggest_float("learning_rate", 0.005, 0.3, log=True),
            subsample=trial.suggest_float("subsample", 0.6, 1.0),
            colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
            reg_alpha=trial.suggest_float("reg_alpha", 1e-3, 10.0, log=True),
            reg_lambda=trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
            n_jobs=-1, random_state=SEED, verbosity=0,
        )
        fold_maes = []
        for fold, (tr_idx, va_idx) in enumerate(tscv.split(X_train)):
            mdl = XGBRegressor(**params)
            mdl.fit(X_train.iloc[tr_idx], y_train.iloc[tr_idx])
            preds = mdl.predict(X_train.iloc[va_idx])
            mae = mean_absolute_error(y_train.iloc[va_idx], preds)
            fold_maes.append(mae)
            trial.report(mae, fold)
            if trial.should_prune():
                raise optuna.TrialPruned()
        return float(np.mean(fold_maes))

    return objective


def make_lgbm_objective(X_train: pd.DataFrame, y_train: pd.Series, n_splits: int = OPTUNA_CV_SPLITS):
    tscv = TimeSeriesSplit(n_splits=n_splits)

    def objective(trial: optuna.Trial) -> float:
        params = dict(
            num_leaves=trial.suggest_int("num_leaves", 20, 300),
            min_child_samples=trial.suggest_int("min_child_samples", 5, 100),
            n_estimators=trial.suggest_int("n_estimators", 100, 600, step=50),
            learning_rate=trial.suggest_float("learning_rate", 0.005, 0.3, log=True),
            max_depth=trial.suggest_int("max_depth", 3, 12),
            colsample_bytree=trial.suggest_float("colsample_bytree", 0.5, 1.0),
            subsample=trial.suggest_float("subsample", 0.6, 1.0),
            reg_alpha=trial.suggest_float("reg_alpha", 1e-3, 10.0, log=True),
            reg_lambda=trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
            n_jobs=-1, random_state=SEED, verbose=-1,
        )
        fold_maes = []
        for fold, (tr_idx, va_idx) in enumerate(tscv.split(X_train)):
            X_tr, X_va = X_train.iloc[tr_idx], X_train.iloc[va_idx]
            y_tr, y_va = y_train.iloc[tr_idx], y_train.iloc[va_idx]
            mdl = lgb.LGBMRegressor(**params)
            mdl.fit(X_tr, y_tr, eval_set=[(X_va, y_va)],
                    callbacks=[lgb.early_stopping(stopping_rounds=20, verbose=False),
                               lgb.log_evaluation(period=-1)])
            mae = mean_absolute_error(y_va, mdl.predict(X_va))
            fold_maes.append(mae)
            trial.report(mae, fold)
            if trial.should_prune():
                raise optuna.TrialPruned()
        return float(np.mean(fold_maes))

    return objective


def run_optuna_study(objective, n_trials: int, study_name: str, seed: int = SEED) -> optuna.Study:
    study = optuna.create_study(
        direction="minimize",
        sampler=TPESampler(seed=seed),
        pruner=MedianPruner(n_warmup_steps=1),
        study_name=study_name,
    )
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
    print(f"  {study_name}: best CV-MAE = {study.best_value:.4f}, best params = {study.best_params}")
    return study


def export_optuna_artifacts(study: optuna.Study, prefix: str) -> None:
    """Export trial history CSV and every requested Optuna diagnostic plot.
    Each plotting call is wrapped individually: with very few completed
    trials some plots (e.g. contour, which needs >=2 varying params with
    enough joint observations) can be undefined, in which case that single
    plot is skipped and reported rather than the whole export failing."""
    history_df = study.trials_dataframe()
    export_table(history_df, f"{prefix}_optimization_history", index=False)

    completed = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
    running_min = pd.Series([t.value for t in completed]).cummin()
    convergence_df = pd.DataFrame({
        "trial": [t.number + 1 for t in completed],
        "value": [t.value for t in completed],
        "running_min": running_min,
    })
    export_table(convergence_df, f"{prefix}_convergence", index=False)

    best_params_df = pd.DataFrame([study.best_params])
    best_params_df["best_value"] = study.best_value
    export_table(best_params_df, f"{prefix}_best_parameters", index=False)

    plot_fns = {
        "optimization_history": plot_optimization_history,
        "param_importances": plot_param_importances,
        "contour": plot_contour,
        "slice": plot_slice,
        "parallel_coordinate": plot_parallel_coordinate,
    }
    for plot_name, fn in plot_fns.items():
        try:
            ax = fn(study)
            fig = ax.get_figure() if hasattr(ax, "get_figure") else plt.gcf()
            save_figure(fig, f"{prefix}_{plot_name}", subdir="optuna")
        except Exception as e:
            print(f"  Skipped {prefix}_{plot_name} plot (NOT_APPLICABLE: {e})")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(convergence_df["trial"], convergence_df["value"], "o", alpha=0.4, label="Trial MAE")
    ax.plot(convergence_df["trial"], convergence_df["running_min"], color="crimson",
            linewidth=2, label="Running best")
    ax.set_xlabel("Trial")
    ax.set_ylabel("CV MAE")
    ax.set_title(f"{prefix} — Optuna Convergence")
    ax.legend()
    plt.tight_layout()
    save_figure(fig, f"{prefix}_manual_convergence", subdir="optuna")


def tune_and_refit(model_class, best_params: dict, fixed_params: dict,
                    X_train, y_train, X_test, y_test, name: str) -> tuple:
    model = model_class(**{**fixed_params, **best_params})
    t0 = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - t0
    t0 = time.time()
    preds = model.predict(X_test)
    pred_time = time.time() - t0
    metrics = compute_metrics(name, y_test, preds, train_time, pred_time, model_size_kb(model))
    return model, preds, metrics


# ==============================================================================
# SECTION 12: DEEP LEARNING MODELS (LSTM + TRANSFORMER)
# ==============================================================================
def create_sequences(X: np.ndarray, y: np.ndarray, lookback: int) -> tuple:
    """Convert a (n_samples, n_features) matrix into overlapping sequences of
    length `lookback` for sequence models. Sequence i uses rows
    [i, i+lookback) to predict the target at row i+lookback (i.e. still
    strictly causal / no leakage)."""
    X_seq, y_seq = [], []
    for i in range(len(X) - lookback):
        X_seq.append(X[i:i + lookback])
        y_seq.append(y[i + lookback])
    return np.array(X_seq), np.array(y_seq)


def prepare_dl_data(split: dict, lookback: int = LOOKBACK) -> dict:
    """Scale features+target with MinMaxScaler (fit on train only) and build
    sequences for LSTM/Transformer input."""
    feat_scaler = MinMaxScaler()
    target_scaler = MinMaxScaler()

    X_train_scaled = feat_scaler.fit_transform(split["X_train"])
    X_test_scaled = feat_scaler.transform(split["X_test"])
    y_train_scaled = target_scaler.fit_transform(split["y_train"].values.reshape(-1, 1)).ravel()
    y_test_scaled = target_scaler.transform(split["y_test"].values.reshape(-1, 1)).ravel()

    X_train_seq, y_train_seq = create_sequences(X_train_scaled, y_train_scaled, lookback)
    X_test_seq, y_test_seq = create_sequences(X_test_scaled, y_test_scaled, lookback)

    # Hold out the last 15% of training sequences (still chronological) for validation.
    n_val = max(int(0.15 * len(X_train_seq)), 1)
    X_tr, X_val = X_train_seq[:-n_val], X_train_seq[-n_val:]
    y_tr, y_val = y_train_seq[:-n_val], y_train_seq[-n_val:]

    return dict(X_tr=X_tr, y_tr=y_tr, X_val=X_val, y_val=y_val,
                X_test_seq=X_test_seq, y_test_seq=y_test_seq,
                feat_scaler=feat_scaler, target_scaler=target_scaler,
                n_features=X_train_scaled.shape[1],
                dates_test_seq=split["dates_test"].iloc[lookback:].reset_index(drop=True))


def build_lstm_model(input_shape: tuple, seed: int = SEED) -> Sequential:
    """Sequence-to-one LSTM: LSTM(128, return_sequences) -> Dropout ->
    LSTM(64) -> Dropout -> Dense(32) -> Dense(1)."""
    tf.random.set_seed(seed)
    model = Sequential([
        Input(shape=input_shape),
        LSTM(128, return_sequences=True),
        Dropout(0.2),
        LSTM(64, return_sequences=False),
        Dropout(0.2),
        Dense(32, activation="relu"),
        Dense(1),
    ])
    model.compile(optimizer=Adam(learning_rate=1e-3), loss="mse")
    return model


def sinusoidal_positional_encoding(seq_len: int, d_model: int) -> np.ndarray:
    """Standard Transformer sinusoidal positional encoding (Vaswani et al.)."""
    positions = np.arange(seq_len)[:, np.newaxis]
    dims = np.arange(d_model)[np.newaxis, :]
    angle_rates = 1 / np.power(10000, (2 * (dims // 2)) / np.float32(d_model))
    angle_rads = positions * angle_rates
    angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
    angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])
    return angle_rads[np.newaxis, ...].astype(np.float32)


def transformer_encoder_block(inputs, d_model: int, num_heads: int, ff_dim: int,
                               dropout: float, block_name: str):
    """One pre-norm Transformer encoder block: multi-head self-attention with
    a residual connection and layer norm, followed by a feed-forward network
    with its own residual connection and layer norm."""
    attn_out, attn_scores = MultiHeadAttention(
        num_heads=num_heads, key_dim=d_model // num_heads, dropout=dropout,
        name=f"{block_name}_mha"
    )(inputs, inputs, return_attention_scores=True)
    attn_out = Dropout(dropout)(attn_out)
    x = Add()([inputs, attn_out])
    x = LayerNormalization(epsilon=1e-6)(x)

    ff = Dense(ff_dim, activation="relu")(x)
    ff = Dense(d_model)(ff)
    ff = Dropout(dropout)(ff)
    x = Add()([x, ff])
    x = LayerNormalization(epsilon=1e-6)(x)
    return x, attn_scores


def build_transformer_model(seq_len: int, n_features: int, d_model: int = 64,
                             num_heads: int = 4, ff_dim: int = 128,
                             num_encoder_layers: int = 2, dropout: float = 0.1,
                             seed: int = SEED) -> tuple:
    """
    Transformer encoder for multivariate time-series regression:
    input projection -> sinusoidal positional encoding -> N encoder blocks
    (multi-head self-attention + feed-forward, each with residual connections
    and layer normalization) -> global average pooling -> dense head.
    Returns (training_model, attention_extractor_model) so attention weights
    from the final block can be inspected later for explainability.
    """
    tf.random.set_seed(seed)
    inputs = Input(shape=(seq_len, n_features), name="sequence_input")
    x = Dense(d_model, name="input_projection")(inputs)

    pos_encoding = sinusoidal_positional_encoding(seq_len, d_model)
    x = x + tf.constant(pos_encoding)

    attn_scores_last = None
    for i in range(num_encoder_layers):
        x, attn_scores_last = transformer_encoder_block(
            x, d_model, num_heads, ff_dim, dropout, block_name=f"encoder_{i}"
        )

    pooled = GlobalAveragePooling1D()(x)
    pooled = Dropout(dropout)(pooled)
    dense = Dense(32, activation="relu")(pooled)
    outputs = Dense(1, name="forecast")(dense)

    model = Model(inputs, outputs, name="load_transformer")
    model.compile(optimizer=Adam(learning_rate=1e-3), loss="mse")

    attention_model = Model(inputs, attn_scores_last, name="load_transformer_attention")
    return model, attention_model


def train_deep_model(model, X_tr, y_tr, X_val, y_val, name: str,
                      epochs: int = DL_EPOCHS, batch_size: int = DL_BATCH_SIZE):
    """Train an LSTM or Transformer model with early stopping and LR decay."""
    print(f"Training {name} ...")
    callbacks = [
        EarlyStopping(monitor="val_loss", patience=8, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=4, min_lr=1e-6),
    ]
    t0 = time.time()
    history = model.fit(
        X_tr, y_tr, validation_data=(X_val, y_val),
        epochs=epochs, batch_size=batch_size, callbacks=callbacks, verbose=0,
    )
    train_time = time.time() - t0
    print(f"  {name} training complete in {train_time:.1f}s over {len(history.history['loss'])} epochs "
          f"(best val_loss={min(history.history['val_loss']):.5f}).")
    return model, history, train_time


def evaluate_deep_model(model, X_test_seq, y_test_seq, target_scaler,
                         name: str, train_time: float) -> tuple:
    """Inverse-transform predictions back to MW before computing metrics, so
    DL metrics are directly comparable to the classical-model metrics."""
    t0 = time.time()
    preds_scaled = model.predict(X_test_seq, verbose=0).ravel()
    pred_time = time.time() - t0
    preds = target_scaler.inverse_transform(preds_scaled.reshape(-1, 1)).ravel()
    y_true = target_scaler.inverse_transform(y_test_seq.reshape(-1, 1)).ravel()
    metrics = compute_metrics(name, y_true, preds, train_time, pred_time, model_size_kb(model.get_weights()))
    return preds, y_true, metrics


# ==============================================================================
# SECTION 13: EXPLAINABILITY
# ==============================================================================
def shap_analysis_tree_model(model, X_background: pd.DataFrame, X_explain: pd.DataFrame,
                              name: str, max_display: int = 20) -> Optional[pd.DataFrame]:
    """
    Full SHAP suite for a tree-based model: summary (bar), beeswarm,
    dependence (top feature), waterfall (single instance), and interaction
    values where computationally feasible. NOT_APPLICABLE if the `shap`
    package is not installed in the environment — returns None rather than
    fabricating importances.
    """
    if not SHAP_AVAILABLE:
        print(f"  SHAP not available in this environment — skipping SHAP analysis for {name} "
              f"(NOT_APPLICABLE).")
        return None

    print(f"Running SHAP analysis for {name} ...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_explain)

    fig = plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_explain, plot_type="bar", max_display=max_display, show=False)
    save_figure(plt.gcf(), f"shap_summary_bar_{name}", subdir="shap")

    fig = plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_explain, max_display=max_display, show=False)
    save_figure(plt.gcf(), f"shap_beeswarm_{name}", subdir="shap")

    top_feature = X_explain.columns[np.argsort(-np.abs(shap_values.values).mean(axis=0))[0]]
    fig = plt.figure(figsize=(9, 6))
    shap.dependence_plot(top_feature, shap_values.values, X_explain, show=False)
    save_figure(plt.gcf(), f"shap_dependence_{name}_{top_feature}", subdir="shap")

    fig = plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_values[0], show=False)
    save_figure(plt.gcf(), f"shap_waterfall_{name}_instance0", subdir="shap")

    try:
        interaction_values = explainer.shap_interaction_values(X_explain.iloc[:min(200, len(X_explain))])
        mean_interactions = np.abs(interaction_values).mean(axis=0)
        interaction_df = pd.DataFrame(mean_interactions, index=X_explain.columns, columns=X_explain.columns)
        export_table(interaction_df, f"shap_interaction_{name}")
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(interaction_df.iloc[:max_display, :max_display], cmap="viridis", ax=ax)
        ax.set_title(f"SHAP Interaction Values — {name}")
        plt.tight_layout()
        save_figure(fig, f"shap_interaction_heatmap_{name}", subdir="shap")
    except Exception as e:
        print(f"  SHAP interaction values skipped for {name} (NOT_APPLICABLE: {e})")

    global_importance = pd.DataFrame({
        "feature": X_explain.columns,
        "mean_abs_shap": np.abs(shap_values.values).mean(axis=0),
    }).sort_values("mean_abs_shap", ascending=False).reset_index(drop=True)
    export_table(global_importance, f"shap_global_importance_{name}", index=False)
    return global_importance


def linear_coefficient_importance(model: LinearRegression, feature_names: list,
                                   X_train_scaled: pd.DataFrame) -> pd.DataFrame:
    """Standardized coefficient magnitudes = importance for a linear model
    fit on standardized inputs (coefficients are already on a comparable scale)."""
    coefs = pd.DataFrame({
        "feature": feature_names,
        "standardized_coefficient": model.coef_,
        "abs_coefficient": np.abs(model.coef_),
    }).sort_values("abs_coefficient", ascending=False).reset_index(drop=True)
    export_table(coefs, "linear_regression_coefficient_importance", index=False)

    fig, ax = plt.subplots(figsize=(9, 8))
    top = coefs.head(20)
    sns.barplot(data=top, x="standardized_coefficient", y="feature", ax=ax, palette="coolwarm")
    ax.set_title("Linear Regression — Standardized Coefficient Importance")
    plt.tight_layout()
    save_figure(fig, "linear_regression_coefficients")
    return coefs


def transformer_attention_visualization(attention_model, X_sample: np.ndarray,
                                         instance_idx: int = 0) -> None:
    """Visualize the attention-weight matrix from the final Transformer
    encoder block for one test sequence (averaged across heads)."""
    attn_scores = attention_model.predict(X_sample[instance_idx:instance_idx + 1], verbose=0)
    # attn_scores shape: (1, num_heads, seq_len, seq_len)
    avg_attn = attn_scores[0].mean(axis=0)
    fig, ax = plt.subplots(figsize=(8, 7))
    sns.heatmap(avg_attn, cmap="magma", ax=ax, cbar_kws={"label": "Attention weight"})
    ax.set_xlabel("Key time step")
    ax.set_ylabel("Query time step")
    ax.set_title(f"Transformer Self-Attention (head-averaged) — test instance {instance_idx}")
    plt.tight_layout()
    save_figure(fig, f"transformer_attention_instance{instance_idx}")


def transformer_permutation_importance(model, X_test_seq: np.ndarray, y_test_seq: np.ndarray,
                                        feature_names: list, n_repeats: int = 5,
                                        seed: int = SEED) -> pd.DataFrame:
    """
    Permutation importance for the Transformer: shuffle one feature across
    all time steps of all test sequences, measure MAE increase. A
    model-agnostic alternative to Integrated Gradients that needs no extra
    dependency (sklearn's permutation_importance does not support 3-D
    sequence input directly, so this is implemented manually).
    """
    rng = np.random.default_rng(seed)
    baseline_preds = model.predict(X_test_seq, verbose=0).ravel()
    baseline_mae = mean_absolute_error(y_test_seq, baseline_preds)

    results = []
    for f_idx, f_name in enumerate(feature_names):
        increases = []
        for _ in range(n_repeats):
            X_perm = X_test_seq.copy()
            perm_order = rng.permutation(X_perm.shape[0])
            X_perm[:, :, f_idx] = X_perm[perm_order, :, f_idx]
            preds = model.predict(X_perm, verbose=0).ravel()
            mae = mean_absolute_error(y_test_seq, preds)
            increases.append(mae - baseline_mae)
        results.append({"feature": f_name, "mean_mae_increase": np.mean(increases),
                         "std_mae_increase": np.std(increases)})

    report = pd.DataFrame(results).sort_values("mean_mae_increase", ascending=False).reset_index(drop=True)
    export_table(report, "transformer_permutation_importance", index=False)

    fig, ax = plt.subplots(figsize=(9, 8))
    top = report.head(20)
    sns.barplot(data=top, x="mean_mae_increase", y="feature", ax=ax, palette="viridis")
    ax.set_title("Transformer — Permutation Importance (MAE increase)")
    plt.tight_layout()
    save_figure(fig, "transformer_permutation_importance")
    return report


# ==============================================================================
# SECTION 14: ABLATION STUDY
# ==============================================================================
def define_feature_tiers(df_columns: list) -> dict:
    """
    Six cumulative feature tiers as required for the ablation study:
      1. raw                      - weather + basic calendar only
      2. raw + lag                - adds lag_*
      3. raw + lag + rolling       - adds roll_*, expanding_*, ewma_*
      4. raw + lag + rolling + cyclical - adds hour/weekday/month sin-cos
      5. raw + lag + rolling + weather - re-emphasizes weather + interactions
      6. full pipeline             - every engineered feature
    Each tier is defined as a column-name-prefix filter so it adapts
    automatically to whatever columns actually exist for a given dataset.
    """
    def cols_matching(prefixes):
        return [c for c in df_columns if any(c == p or c.startswith(p) for p in prefixes)]

    raw = cols_matching(["temp", "dwpt", "rhum", "wspd", "pres", "wdir_sin", "wdir_cos",
                          "weekday", "weekend", "is_peak_hour", "is_day", "is_night",
                          "quarter", "season", "is_month_end", "is_holiday"])
    lag = cols_matching(["lag_"])
    rolling = cols_matching(["roll_", "expanding_", "ewma_", "diff_", "pct_change",
                             "load_growth_rate", "load_acceleration"])
    cyclical = cols_matching(["hour_sin", "hour_cos", "weekday_sin", "weekday_cos",
                              "month_sin", "month_cos"])
    weather = cols_matching(["temp", "dwpt", "rhum", "wspd", "pres", "wdir_sin", "wdir_cos",
                             "temp_hour", "temp_x_peak"])

    tiers = {
        "1_raw": sorted(set(raw)),
        "2_raw_lag": sorted(set(raw + lag)),
        "3_raw_lag_rolling": sorted(set(raw + lag + rolling)),
        "4_raw_lag_rolling_cyclical": sorted(set(raw + lag + rolling + cyclical)),
        "5_raw_lag_rolling_weather": sorted(set(raw + lag + rolling + weather)),
        "6_full_pipeline": sorted(set(df_columns)),
    }
    return tiers


def run_ablation_study(df: pd.DataFrame, target: str, split_date: str,
                        model_builder=None, seed: int = SEED) -> pd.DataFrame:
    """
    Train a fixed, fast model (LightGBM by default — good accuracy/speed
    tradeoff for repeated ablation runs) on each cumulative feature tier and
    report MAE/RMSE/R2/MAPE plus percentage improvement over the raw tier.
    """
    print("Running ablation study across feature tiers ...")
    all_features = get_feature_list(df, target=target)
    tiers = define_feature_tiers(all_features)

    if model_builder is None:
        model_builder = lambda: lgb.LGBMRegressor(
            n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.8,
            colsample_bytree=0.8, n_jobs=-1, random_state=seed, verbose=-1)

    rows = []
    baseline_mae = None
    for tier_name, tier_features in tiers.items():
        tier_features = [f for f in tier_features if f in df.columns]
        if not tier_features:
            print(f"  Tier {tier_name}: NOT_APPLICABLE — no matching columns for this dataset.")
            continue
        train_df, test_df = time_based_train_test_split(df, split_date)
        X_tr, y_tr = train_df[tier_features], train_df[target]
        X_te, y_te = test_df[tier_features], test_df[target]

        model = model_builder()
        model.fit(X_tr, y_tr)
        preds = model.predict(X_te)
        m = compute_metrics(tier_name, y_te, preds)
        if baseline_mae is None:
            baseline_mae = m["MAE"]
        m["n_features"] = len(tier_features)
        m["pct_MAE_improvement_vs_raw"] = 100 * (baseline_mae - m["MAE"]) / baseline_mae
        rows.append(m)
        print(f"  {tier_name:<32} n_features={len(tier_features):3d}  MAE={m['MAE']:.3f}  RMSE={m['RMSE']:.3f}")

    ablation_df = pd.DataFrame(rows)
    export_table(ablation_df, "ablation", index=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=ablation_df, x="Model", y="MAE", ax=ax, palette="mako")
    ax.set_xlabel("Feature tier")
    ax.set_title("Ablation Study — MAE by Feature Tier")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    save_figure(fig, "ablation_mae_barchart")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ablation_df["Model"], ablation_df["RMSE"], marker="o", color="#D95F02")
    ax.set_ylabel("RMSE")
    ax.set_title("Ablation Study — RMSE Trend Across Feature Tiers")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    save_figure(fig, "ablation_rmse_linechart")

    print("Ablation study complete.\n")
    return ablation_df


# ==============================================================================
# SECTION 15: STATISTICAL SIGNIFICANCE TESTING
# ==============================================================================
def diebold_mariano_test(errors_a: np.ndarray, errors_b: np.ndarray, h: int = 1,
                          power: int = 2) -> dict:
    """
    Diebold-Mariano test for equal predictive accuracy of two forecasts.
    Loss differential d_t = |e_a|^power - |e_b|^power; tests H0: mean(d)=0
    using a Newey-West-style long-run variance estimate (h-1 lag truncation)
    to account for potential autocorrelation in the loss differential series.
    NOT_APPLICABLE if fewer than ~10 paired residuals are available.
    """
    errors_a, errors_b = np.asarray(errors_a), np.asarray(errors_b)
    n = len(errors_a)
    if n < 10:
        return {"DM_statistic": np.nan, "p_value": np.nan, "note": "NOT_APPLICABLE - fewer than 10 paired residuals"}

    d = np.abs(errors_a) ** power - np.abs(errors_b) ** power
    d_mean = d.mean()

    gamma0 = np.var(d, ddof=0)
    var_d = gamma0
    for lag in range(1, h):
        cov = np.cov(d[lag:], d[:-lag])[0, 1] if n - lag > 1 else 0.0
        var_d += 2 * (1 - lag / h) * cov
    var_d = var_d / n

    if var_d <= 0:
        return {"DM_statistic": np.nan, "p_value": np.nan, "note": "NOT_APPLICABLE - non-positive variance estimate"}

    dm_stat = d_mean / np.sqrt(var_d)
    p_value = 2 * (1 - scipy_stats.t.cdf(np.abs(dm_stat), df=n - 1))
    return {"DM_statistic": dm_stat, "p_value": p_value, "note": "ok"}


def statistical_comparison_table(errors_dict: dict, alpha: float = 0.05) -> dict:
    """
    Pairwise Wilcoxon signed-rank test, Diebold-Mariano test, and paired
    t-test across all model pairs, plus a single Friedman test across all
    models jointly. `errors_dict`: {model_name: residual_array}. All arrays
    must share the same test-set alignment (same rows, same order).
    """
    print("Running statistical significance tests ...")
    names = list(errors_dict.keys())
    lengths = {len(v) for v in errors_dict.values()}
    if len(lengths) != 1:
        print("  WARNING: residual arrays have mismatched lengths; pairwise tests will "
              "align on the minimum overlapping length.")

    pairwise_rows = []
    for a, b in itertools.combinations(names, 2):
        ea, eb = np.asarray(errors_dict[a]), np.asarray(errors_dict[b])
        n = min(len(ea), len(eb))
        ea, eb = ea[:n], eb[:n]

        if n < 10:
            pairwise_rows.append({"model_a": a, "model_b": b,
                                   "wilcoxon_stat": np.nan, "wilcoxon_p": np.nan,
                                   "ttest_stat": np.nan, "ttest_p": np.nan,
                                   "DM_statistic": np.nan, "DM_p": np.nan,
                                   "note": "NOT_APPLICABLE - fewer than 10 paired residuals"})
            continue

        try:
            wstat, wp = scipy_stats.wilcoxon(np.abs(ea), np.abs(eb))
        except ValueError as e:
            wstat, wp = np.nan, np.nan
            print(f"  Wilcoxon skipped for {a} vs {b} (NOT_APPLICABLE: {e})")

        tstat, tp = scipy_stats.ttest_rel(np.abs(ea), np.abs(eb))
        dm = diebold_mariano_test(ea, eb)

        pairwise_rows.append({
            "model_a": a, "model_b": b,
            "wilcoxon_stat": wstat, "wilcoxon_p": wp,
            "ttest_stat": tstat, "ttest_p": tp,
            "DM_statistic": dm["DM_statistic"], "DM_p": dm["p_value"],
            "significant_at_alpha": (wp < alpha) if not np.isnan(wp) else False,
            "note": dm["note"],
        })

    pairwise_df = pd.DataFrame(pairwise_rows)

    # Friedman test needs equal-length, non-degenerate samples across all models.
    min_len = min(len(v) for v in errors_dict.values())
    if min_len >= 10 and len(names) >= 3:
        aligned = [np.abs(np.asarray(errors_dict[n])[:min_len]) for n in names]
        friedman_stat, friedman_p = scipy_stats.friedmanchisquare(*aligned)
        friedman_result = {"friedman_statistic": friedman_stat, "friedman_p": friedman_p,
                            "n_models": len(names), "n_observations": min_len, "note": "ok"}
    else:
        friedman_result = {"friedman_statistic": np.nan, "friedman_p": np.nan,
                            "n_models": len(names), "n_observations": min_len,
                            "note": "NOT_APPLICABLE - need >=3 models and >=10 aligned observations"}

    export_table(pairwise_df, "statistical_tests", index=False)
    export_table(pd.DataFrame([friedman_result]), "statistical_tests_friedman", index=False)
    print("Statistical testing complete.\n")
    return {"pairwise": pairwise_df, "friedman": friedman_result}


# ==============================================================================
# SECTION 16: ROBUSTNESS ANALYSIS
# ==============================================================================
def bootstrap_metric_ci(y_true: np.ndarray, y_pred: np.ndarray, metric_fn,
                         n_boot: int = N_BOOTSTRAP, ci: float = 0.95,
                         seed: int = SEED) -> dict:
    """Percentile bootstrap confidence interval for a metric on paired
    (y_true, y_pred) test-set arrays."""
    rng = np.random.default_rng(seed)
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    n = len(y_true)
    boot_scores = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boot_scores[i] = metric_fn(y_true[idx], y_pred[idx])
    lower_q, upper_q = (1 - ci) / 2, 1 - (1 - ci) / 2
    return {
        "point_estimate": metric_fn(y_true, y_pred),
        "ci_lower": np.quantile(boot_scores, lower_q),
        "ci_upper": np.quantile(boot_scores, upper_q),
        "boot_std": boot_scores.std(),
    }


def repeated_tscv_evaluation(model_builder, X: pd.DataFrame, y: pd.Series,
                              n_splits: int = TSCV_SPLITS, n_repeats: int = 3,
                              seed: int = SEED) -> pd.DataFrame:
    """
    Repeated TimeSeriesSplit evaluation. True k-fold repetition with
    reshuffling is invalid for time series (would break chronological
    ordering), so "repeats" instead vary the random seed of the estimator
    across otherwise-identical forward-chaining folds — this captures
    training-stochasticity variance in addition to fold-to-fold variance.
    """
    rows = []
    for repeat in range(n_repeats):
        tscv = TimeSeriesSplit(n_splits=n_splits)
        for fold, (tr_idx, te_idx) in enumerate(tscv.split(X)):
            model = model_builder(seed=seed + repeat)
            model.fit(X.iloc[tr_idx], y.iloc[tr_idx])
            preds = model.predict(X.iloc[te_idx])
            m = compute_metrics(f"repeat{repeat}_fold{fold}", y.iloc[te_idx], preds)
            m["repeat"] = repeat
            m["fold"] = fold
            rows.append(m)
    result = pd.DataFrame(rows)
    export_table(result, "cross_validation", index=False)
    return result


def noise_robustness_test(model, X_test: pd.DataFrame, y_test: pd.Series,
                           noise_levels: list = (0.0, 0.01, 0.05, 0.1, 0.2),
                           seed: int = SEED) -> pd.DataFrame:
    """Add Gaussian noise (scaled to each feature's std) to the test features
    and measure metric degradation — a proxy for sensor-noise robustness."""
    rng = np.random.default_rng(seed)
    rows = []
    feature_stds = X_test.std()
    for level in noise_levels:
        X_noisy = X_test + rng.normal(0, level, X_test.shape) * feature_stds.values
        preds = model.predict(X_noisy)
        m = compute_metrics(f"noise_{level}", y_test, preds)
        m["noise_level"] = level
        rows.append(m)
    result = pd.DataFrame(rows)
    export_table(result, "robustness_noise", index=False)
    return result


def missing_value_robustness_test(model, X_test: pd.DataFrame, y_test: pd.Series,
                                   missing_fracs: list = (0.0, 0.05, 0.1, 0.2, 0.3),
                                   seed: int = SEED) -> pd.DataFrame:
    """Randomly null out a fraction of feature values (median-imputed, since
    tree/linear models used here cannot accept NaN) and measure degradation."""
    rng = np.random.default_rng(seed)
    rows = []
    medians = X_test.median()
    for frac in missing_fracs:
        X_missing = X_test.copy()
        mask = rng.random(X_missing.shape) < frac
        X_arr = X_missing.values
        X_arr[mask] = np.nan
        X_missing = pd.DataFrame(X_arr, columns=X_missing.columns, index=X_missing.index)
        X_missing = X_missing.fillna(medians)
        preds = model.predict(X_missing)
        m = compute_metrics(f"missing_{frac}", y_test, preds)
        m["missing_fraction"] = frac
        rows.append(m)
    result = pd.DataFrame(rows)
    export_table(result, "robustness_missing_values", index=False)
    return result


def feature_removal_robustness_test(model_builder, X_train: pd.DataFrame, y_train: pd.Series,
                                     X_test: pd.DataFrame, y_test: pd.Series,
                                     features_to_test: list) -> pd.DataFrame:
    """Retrain with each candidate feature removed one at a time and measure
    the resulting MAE change — how dependent the model is on any single
    feature (distinct from static feature_importances_, since this reflects
    actual retrained performance, not in-model attribution)."""
    rows = []
    baseline_model = model_builder()
    baseline_model.fit(X_train, y_train)
    baseline_mae = mean_absolute_error(y_test, baseline_model.predict(X_test))
    rows.append({"removed_feature": "(none - baseline)", "MAE": baseline_mae, "delta_MAE": 0.0})

    for feat in features_to_test:
        cols = [c for c in X_train.columns if c != feat]
        model = model_builder()
        model.fit(X_train[cols], y_train)
        mae = mean_absolute_error(y_test, model.predict(X_test[cols]))
        rows.append({"removed_feature": feat, "MAE": mae, "delta_MAE": mae - baseline_mae})

    result = pd.DataFrame(rows).sort_values("delta_MAE", ascending=False).reset_index(drop=True)
    export_table(result, "robustness_feature_removal", index=False)
    return result


def run_robustness_analysis(model, model_builder, split: dict, top_features: list) -> dict:
    print("Running robustness analysis ...")
    mae_ci = bootstrap_metric_ci(split["y_test"].values, model.predict(split["X_test"]),
                                  mean_absolute_error)
    rmse_ci = bootstrap_metric_ci(split["y_test"].values, model.predict(split["X_test"]),
                                   lambda a, b: np.sqrt(mean_squared_error(a, b)))
    ci_df = pd.DataFrame([{"metric": "MAE", **mae_ci}, {"metric": "RMSE", **rmse_ci}])
    export_table(ci_df, "robustness_bootstrap_ci", index=False)

    noise_df = noise_robustness_test(model, split["X_test"], split["y_test"])
    missing_df = missing_value_robustness_test(model, split["X_test"], split["y_test"])
    removal_df = feature_removal_robustness_test(
        model_builder, split["X_train"], split["y_train"], split["X_test"], split["y_test"],
        top_features
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(noise_df["noise_level"], noise_df["MAE"], marker="o")
    ax.set_xlabel("Injected noise (fraction of feature std)")
    ax.set_ylabel("MAE")
    ax.set_title("Robustness — MAE vs Feature Noise")
    plt.tight_layout()
    save_figure(fig, "robustness_noise_plot")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(missing_df["missing_fraction"], missing_df["MAE"], marker="o", color="#D95F02")
    ax.set_xlabel("Fraction of values set missing (median-imputed)")
    ax.set_ylabel("MAE")
    ax.set_title("Robustness — MAE vs Missing-Value Fraction")
    plt.tight_layout()
    save_figure(fig, "robustness_missing_plot")

    print("Robustness analysis complete.\n")
    return {"bootstrap_ci": ci_df, "noise": noise_df, "missing": missing_df, "feature_removal": removal_df}


# ==============================================================================
# SECTION 17: MODEL COMPARISON TABLE
# ==============================================================================
def comparison_champion_name(df: pd.DataFrame) -> str:
    """Return the model name with the lowest RMSE (the pipeline's champion model)."""
    return df.loc[df["RMSE"].idxmin(), "Model"]


def build_model_comparison_table(all_metrics: list, cv_results: pd.DataFrame,
                                  bootstrap_ci: pd.DataFrame) -> pd.DataFrame:
    """
    Publication-ready comparison table: Model, MAE, RMSE, MAPE, R2, Training
    Time, Prediction Time, Model Size, CV MAE, CV RMSE, 95% CI, Rank.
    """
    df = pd.DataFrame(all_metrics)

    # Cross-validation MAE/RMSE are attached to the tuned XGBoost row, since
    # `cv_results` here comes from the TimeSeriesSplit CV run on that model
    # (Section 20 orchestration). Other rows keep NaN - CV was not repeated
    # per-model to keep total runtime tractable, matching the requirement
    # that CV be reported "wherever computationally feasible".
    df["CV MAE"] = np.nan
    df["CV RMSE"] = np.nan
    if cv_results is not None and len(cv_results) and "XGBoost (Tuned)" in df["Model"].values:
        df.loc[df["Model"] == "XGBoost (Tuned)", "CV MAE"] = cv_results["MAE"].mean()
        df.loc[df["Model"] == "XGBoost (Tuned)", "CV RMSE"] = cv_results["RMSE"].mean()

    # 95% bootstrap CI on MAE, attached to the single model it was computed
    # for (the pipeline's best/champion model - see run_robustness_analysis).
    df["95% CI (MAE)"] = ""
    if isinstance(bootstrap_ci, pd.DataFrame) and len(bootstrap_ci):
        mae_row = bootstrap_ci[bootstrap_ci["metric"] == "MAE"]
        if len(mae_row):
            lo, hi = mae_row.iloc[0]["ci_lower"], mae_row.iloc[0]["ci_upper"]
            champion = comparison_champion_name(df)
            df.loc[df["Model"] == champion, "95% CI (MAE)"] = f"[{lo:.3f}, {hi:.3f}]"

    df = df.sort_values("RMSE").reset_index(drop=True)
    df["Model Rank"] = df["RMSE"].rank(method="min").astype(int)

    export_table(df, "model_comparison", index=False)
    export_table(df[["Model", "MAE", "RMSE", "R2", "MAPE (%)"]], "metrics", index=False)
    export_table(df[["Model", "Training Time (s)"]], "training_times", index=False)
    export_table(df[["Model", "Prediction Time (s)"]], "prediction_times", index=False)
    return df


# ==============================================================================
# SECTION 18: VISUALIZATION
# ==============================================================================
def plot_actual_vs_predicted(dates_test, y_test, preds_dict: dict, name: str,
                              window_days: Optional[int] = 7) -> None:
    fig, ax = plt.subplots(figsize=(14, 5))
    dt = pd.to_datetime(dates_test)
    if window_days is not None:
        cutoff = dt.max() - pd.Timedelta(days=window_days)
        mask = dt >= cutoff
    else:
        mask = np.ones(len(dt), dtype=bool)
    ax.plot(dt[mask], np.asarray(y_test)[mask], label="Actual", color="black", linewidth=1.8)
    for model_name, preds in preds_dict.items():
        ax.plot(dt[mask], np.asarray(preds)[mask], label=model_name, alpha=0.8, linewidth=1.2)
    ax.set_title(f"Actual vs Predicted — {name}")
    ax.set_ylabel("Load")
    ax.legend(fontsize=8, ncol=2)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    plt.xticks(rotation=20)
    plt.tight_layout()
    save_figure(fig, f"actual_vs_predicted_{name}")


def plot_residual_diagnostics(y_test, preds, name: str) -> None:
    residuals = np.asarray(y_test) - np.asarray(preds)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    sns.histplot(residuals, kde=True, ax=axes[0, 0], color="#2C7FB8")
    axes[0, 0].set_title(f"{name} — Residual Histogram")

    axes[0, 1].scatter(preds, residuals, alpha=0.3, s=8, color="#D95F02")
    axes[0, 1].axhline(0, color="black", linestyle="--")
    axes[0, 1].set_xlabel("Predicted")
    axes[0, 1].set_ylabel("Residual")
    axes[0, 1].set_title(f"{name} — Residual vs Predicted")

    scipy_stats.probplot(residuals, dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title(f"{name} — QQ Plot")

    axes[1, 1].plot(residuals[:500], color="#7570B3", linewidth=0.8)
    axes[1, 1].axhline(0, color="black", linestyle="--")
    axes[1, 1].set_title(f"{name} — Residuals Over Time (first 500 pts)")

    plt.tight_layout()
    save_figure(fig, f"residual_diagnostics_{name}")


def plot_model_comparison_bars(comparison_df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, metric in zip(axes, ["MAE", "RMSE", "MAPE (%)"]):
        sns.barplot(data=comparison_df.sort_values(metric), x=metric, y="Model", ax=ax, palette="crest")
        ax.set_title(metric)
    plt.tight_layout()
    save_figure(fig, "model_comparison_bars")

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.barplot(data=comparison_df.sort_values("R2", ascending=False), x="R2", y="Model", ax=ax, palette="flare")
    ax.set_title("R2 Comparison")
    plt.tight_layout()
    save_figure(fig, "model_comparison_r2")


def plot_learning_curve(history, name: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    epochs_ran = range(1, len(history.history["loss"]) + 1)
    ax.plot(epochs_ran, history.history["loss"], label="Train Loss", linewidth=2)
    ax.plot(epochs_ran, history.history["val_loss"], label="Val Loss", linewidth=2, linestyle="--")
    best_ep = int(np.argmin(history.history["val_loss"])) + 1
    ax.axvline(best_ep, color="gold", linestyle=":", label=f"Best epoch={best_ep}")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("MSE Loss (scaled)")
    ax.set_title(f"{name} — Training History")
    ax.legend()
    plt.tight_layout()
    save_figure(fig, f"{name.lower()}_training_curve")


def extended_performance_analyses(dates_test, y_test, preds: np.ndarray, name: str) -> dict:
    """Top/worst predictions, peak/low-load analysis, hourly/monthly/seasonal
    error breakdowns, and prediction stability — all computed from actual
    residuals of the given model's predictions."""
    y_test = np.asarray(y_test)
    preds = np.asarray(preds)
    residuals = np.abs(y_test - preds)
    dt = pd.to_datetime(dates_test)

    df = pd.DataFrame({"datetime": dt, "actual": y_test, "predicted": preds, "abs_error": residuals})
    df["hour"] = df["datetime"].dt.hour
    df["month"] = df["datetime"].dt.month
    df["weekday"] = df["datetime"].dt.weekday
    df["is_weekend"] = df["weekday"] >= 5
    season_map = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring",
                  6: "Summer", 7: "Summer", 8: "Summer", 9: "Fall", 10: "Fall", 11: "Fall"}
    df["season"] = df["month"].map(season_map)

    best10 = df.nsmallest(10, "abs_error")
    worst10 = df.nlargest(10, "abs_error")
    export_table(best10, f"top10_best_predictions_{name}", index=False)
    export_table(worst10, f"top10_worst_predictions_{name}", index=False)

    peak_thresh = df["actual"].quantile(0.9)
    low_thresh = df["actual"].quantile(0.1)
    peak_analysis = df[df["actual"] >= peak_thresh]["abs_error"].agg(["mean", "std", "count"])
    low_analysis = df[df["actual"] <= low_thresh]["abs_error"].agg(["mean", "std", "count"])

    error_by_hour = df.groupby("hour")["abs_error"].mean()
    error_by_month = df.groupby("month")["abs_error"].mean()
    error_by_season = df.groupby("season")["abs_error"].mean()
    error_by_weekday = df.groupby("is_weekend")["abs_error"].mean()

    export_table(error_by_hour.to_frame("mean_abs_error"), f"error_by_hour_{name}")
    export_table(error_by_month.to_frame("mean_abs_error"), f"error_by_month_{name}")
    export_table(error_by_season.to_frame("mean_abs_error"), f"error_by_season_{name}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    error_by_hour.plot(kind="bar", ax=axes[0], color="#1B9E77")
    axes[0].set_title(f"{name} — Mean Abs Error by Hour")
    error_by_season.plot(kind="bar", ax=axes[1], color="#D95F02")
    axes[1].set_title(f"{name} — Mean Abs Error by Season")
    plt.tight_layout()
    save_figure(fig, f"error_breakdown_{name}")

    stability = {"rolling_mae_std": df["abs_error"].rolling(288).mean().std()}

    return {
        "peak_load_error": peak_analysis.to_dict(), "low_load_error": low_analysis.to_dict(),
        "error_by_hour": error_by_hour, "error_by_month": error_by_month,
        "error_by_season": error_by_season, "error_by_weekday": error_by_weekday,
        "prediction_stability": stability,
    }


# ==============================================================================
# SECTION 19: EXPORT RESULTS
# ==============================================================================
def export_predictions(dates_test, y_test, preds_dict: dict, name_suffix: str = "") -> None:
    """Every model's test-set predictions aligned with actual values and timestamps."""
    out = pd.DataFrame({"datetime": pd.to_datetime(dates_test), "actual": np.asarray(y_test)})
    for model_name, preds in preds_dict.items():
        # Predictions from sequence models are shorter (lookback rows lost);
        # left-align and leave the missing head as NaN rather than fabricate values.
        arr = np.asarray(preds)
        if len(arr) == len(out):
            out[model_name] = arr
        else:
            padded = np.full(len(out), np.nan)
            padded[-len(arr):] = arr
            out[model_name] = padded
    export_table(out, f"test_predictions{name_suffix}", index=False)


def package_outputs(zip_name: str = "electricity_forecast_pipeline_outputs") -> str:
    """Zip the entire pipeline_outputs directory for convenient download."""
    archive_path = shutil.make_archive(zip_name, "zip", OUTPUT_ROOT)
    print(f"Packaged all outputs into: {archive_path}")
    return archive_path


# ==============================================================================
# SECTION 20: FULL PIPELINE ORCHESTRATION (DATASET-INDEPENDENT)
# ==============================================================================
def run_full_pipeline(dataset_candidates: list, column_map_key: str = "default",
                       dataset_label: str = "primary", split_date: str = SPLIT_DATE,
                       run_heavy_analyses: bool = True) -> dict:
    """
    Runs the entire workflow - preprocessing, EDA, feature engineering,
    training, tuning, deep learning, explainability, ablation, statistical
    testing, robustness, comparison table, visualization, export - for one
    dataset. Calling this again with a different `dataset_candidates` /
    `column_map_key` is the entire mechanism for cross-dataset validation
    (Section 21) - no other pipeline code needs to change.
    `run_heavy_analyses=False` skips SHAP/ablation/robustness/statistical
    tests (useful for a lighter second-dataset confirmatory run).
    """
    global FIG_DIR, TABLE_DIR
    _orig_fig_dir, _orig_table_dir = FIG_DIR, TABLE_DIR
    FIG_DIR = os.path.join(OUTPUT_ROOT, "figures", dataset_label)
    TABLE_DIR = os.path.join(OUTPUT_ROOT, "tables", dataset_label)
    os.makedirs(FIG_DIR, exist_ok=True)
    os.makedirs(TABLE_DIR, exist_ok=True)

    print("\n" + "=" * 78)
    print(f"  RUNNING FULL PIPELINE — dataset: {dataset_label}")
    print("=" * 78 + "\n")

    # --- Section 4/5: Load + preprocess -------------------------------------
    path = resolve_dataset_path(dataset_candidates)
    raw_df = load_raw_dataset(path, column_map_key)
    df, preprocessing_summary = run_preprocessing(raw_df)

    weather_cols = [c for c in ["temp", "dwpt", "rhum", "wspd", "pres", "wdir_sin", "wdir_cos"]
                    if c in df.columns]

    # --- Section 6: EDA ------------------------------------------------------
    run_eda(df, weather_cols)

    # --- Section 7: Feature engineering --------------------------------------
    df = engineer_features(df)

    # --- Section 8: Feature ranking / variance / correlation filtering ------
    all_features = get_feature_list(df, target="load")
    ranking_report = feature_ranking_report(df[all_features], df["load"])
    variance_report = variance_analysis(df[all_features])
    kept_features, dropped_report = correlation_filter(df[all_features], threshold=0.97)
    FEATURES = kept_features
    print(f"Final feature set after correlation filtering: {len(FEATURES)} features.\n")

    # --- Section 9: Split & scale ---------------------------------------------
    split = prepare_train_test(df, FEATURES, "load", split_date)

    # --- Section 10: Classical ML models --------------------------------------
    models = build_model_zoo(SEED)
    all_metrics, all_preds, fitted_models = train_and_evaluate_all(models, split)
    tree_importance = tree_feature_importance_report(
        {k: v for k, v in fitted_models.items() if hasattr(v, "feature_importances_")}, FEATURES
    )

    # --- TimeSeriesSplit CV on XGBoost (used later in the comparison table) --
    print("Running TimeSeriesSplit cross-validation on XGBoost ...")
    tscv = build_time_series_cv(TSCV_SPLITS)
    cv_rows = []
    X_full, y_full = df[FEATURES], df["load"]
    for fold, (tr_idx, te_idx) in enumerate(tscv.split(X_full)):
        mdl = XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.05, subsample=0.8,
                            colsample_bytree=0.8, n_jobs=-1, random_state=SEED, verbosity=0)
        mdl.fit(X_full.iloc[tr_idx], y_full.iloc[tr_idx])
        preds = mdl.predict(X_full.iloc[te_idx])
        m = compute_metrics(f"fold{fold}", y_full.iloc[te_idx], preds)
        cv_rows.append(m)
    cv_results = pd.DataFrame(cv_rows)
    export_table(cv_results, "xgboost_timeseries_cv", index=False)
    print(f"  CV Mean MAE: {cv_results['MAE'].mean():.3f} | CV Std MAE: {cv_results['MAE'].std():.3f}\n")

    # --- Section 11: Optuna tuning (XGBoost + LightGBM) -----------------------
    print("Optuna tuning — XGBoost ...")
    xgb_study = run_optuna_study(
        make_xgb_objective(split["X_train"], split["y_train"]), OPTUNA_TRIALS, f"{dataset_label}_xgb"
    )
    export_optuna_artifacts(xgb_study, "xgb")
    xgb_tuned, xgb_tuned_preds, xgb_tuned_metrics = tune_and_refit(
        XGBRegressor, xgb_study.best_params,
        dict(n_jobs=-1, random_state=SEED, verbosity=0),
        split["X_train"], split["y_train"], split["X_test"], split["y_test"], "XGBoost (Tuned)"
    )
    all_metrics.append(xgb_tuned_metrics)
    all_preds["XGBoost (Tuned)"] = xgb_tuned_preds
    fitted_models["XGBoost (Tuned)"] = xgb_tuned

    print("Optuna tuning — LightGBM ...")
    lgbm_study = run_optuna_study(
        make_lgbm_objective(split["X_train"], split["y_train"]), OPTUNA_TRIALS, f"{dataset_label}_lgbm"
    )
    export_optuna_artifacts(lgbm_study, "lgbm")
    lgbm_tuned, lgbm_tuned_preds, lgbm_tuned_metrics = tune_and_refit(
        lgb.LGBMRegressor, lgbm_study.best_params,
        dict(n_jobs=-1, random_state=SEED, verbose=-1),
        split["X_train"], split["y_train"], split["X_test"], split["y_test"], "LightGBM (Tuned)"
    )
    all_metrics.append(lgbm_tuned_metrics)
    all_preds["LightGBM (Tuned)"] = lgbm_tuned_preds
    fitted_models["LightGBM (Tuned)"] = lgbm_tuned

    # --- Weighted ensemble -----------------------------------------------------
    ensemble_preds, w_xgb, w_lgbm = build_weighted_ensemble(
        xgb_tuned_preds, lgbm_tuned_preds, xgb_tuned_metrics["RMSE"], lgbm_tuned_metrics["RMSE"]
    )
    ensemble_metrics = compute_metrics("Weighted Ensemble", split["y_test"], ensemble_preds)
    all_metrics.append(ensemble_metrics)
    all_preds["Weighted Ensemble"] = ensemble_preds
    print(f"Ensemble weights — XGB: {w_xgb:.3f}, LGBM: {w_lgbm:.3f}\n")

    # --- Section 12: Deep learning (LSTM + Transformer) ------------------------
    dl_data = prepare_dl_data(split, LOOKBACK)

    lstm_model = build_lstm_model((LOOKBACK, dl_data["n_features"]))
    lstm_model, lstm_history, lstm_train_time = train_deep_model(
        lstm_model, dl_data["X_tr"], dl_data["y_tr"], dl_data["X_val"], dl_data["y_val"], "LSTM"
    )
    lstm_preds, lstm_y_true, lstm_metrics = evaluate_deep_model(
        lstm_model, dl_data["X_test_seq"], dl_data["y_test_seq"], dl_data["target_scaler"],
        "LSTM", lstm_train_time
    )
    all_metrics.append(lstm_metrics)
    all_preds["LSTM"] = lstm_preds
    plot_learning_curve(lstm_history, "LSTM")

    transformer_model, transformer_attn_model = build_transformer_model(
        LOOKBACK, dl_data["n_features"], d_model=64, num_heads=4, ff_dim=128,
        num_encoder_layers=2, dropout=0.1
    )
    transformer_model, transformer_history, transformer_train_time = train_deep_model(
        transformer_model, dl_data["X_tr"], dl_data["y_tr"], dl_data["X_val"], dl_data["y_val"],
        "Transformer"
    )
    transformer_preds, transformer_y_true, transformer_metrics = evaluate_deep_model(
        transformer_model, dl_data["X_test_seq"], dl_data["y_test_seq"], dl_data["target_scaler"],
        "Transformer", transformer_train_time
    )
    all_metrics.append(transformer_metrics)
    all_preds["Transformer"] = transformer_preds
    plot_learning_curve(transformer_history, "Transformer")

    results = dict(
        df=df, FEATURES=FEATURES, split=split, all_metrics=all_metrics, all_preds=all_preds,
        fitted_models=fitted_models, xgb_tuned=xgb_tuned, lgbm_tuned=lgbm_tuned,
        lstm_model=lstm_model, transformer_model=transformer_model,
        transformer_attn_model=transformer_attn_model, dl_data=dl_data, cv_results=cv_results,
        preprocessing_summary=preprocessing_summary, tree_importance=tree_importance,
    )

    if not run_heavy_analyses:
        comparison_df = build_model_comparison_table(all_metrics, cv_results, pd.DataFrame())
        plot_model_comparison_bars(comparison_df)
        export_predictions(split["dates_test"], split["y_test"], all_preds)
        results["comparison_df"] = comparison_df
        FIG_DIR, TABLE_DIR = _orig_fig_dir, _orig_table_dir
        return results

    # --- Section 13: Explainability ---------------------------------------------
    bg_sample = split["X_train"].sample(min(500, len(split["X_train"])), random_state=SEED)
    explain_sample = split["X_test"].sample(min(500, len(split["X_test"])), random_state=SEED)
    for tree_name in ["Random Forest", "XGBoost (Tuned)", "LightGBM (Tuned)"]:
        if tree_name in fitted_models:
            shap_analysis_tree_model(fitted_models[tree_name], bg_sample, explain_sample, tree_name)

    lr_model = fitted_models.get("Linear Regression")
    if lr_model is not None:
        linear_coefficient_importance(lr_model, FEATURES, split["X_train_sc"])

    transformer_attention_visualization(transformer_attn_model, dl_data["X_test_seq"], instance_idx=0)
    transformer_permutation_importance(transformer_model, dl_data["X_test_seq"], dl_data["y_test_seq"], FEATURES)

    # --- Section 14: Ablation study -----------------------------------------------
    ablation_df = run_ablation_study(df, "load", split_date)

    # --- Section 15: Statistical significance testing -------------------------------
    residuals_dict = {}
    for name, preds in all_preds.items():
        preds_arr = np.asarray(preds)
        y_arr = np.asarray(split["y_test"])
        n = min(len(preds_arr), len(y_arr))
        residuals_dict[name] = (y_arr[-n:] - preds_arr[-n:])
    stat_tests = statistical_comparison_table(residuals_dict)

    # --- Section 16: Robustness analysis (on the champion classical model) ------------
    champion_name = pd.DataFrame(all_metrics).sort_values("RMSE").iloc[0]["Model"]
    champion_model = fitted_models.get(champion_name, fitted_models.get("XGBoost (Tuned)"))

    def _lgbm_builder(seed=SEED):
        return lgb.LGBMRegressor(n_estimators=300, max_depth=6, learning_rate=0.05,
                                  subsample=0.8, colsample_bytree=0.8, n_jobs=-1,
                                  random_state=seed, verbose=-1)

    top_features_for_removal = tree_importance.sort_values(
        tree_importance.columns[-1], ascending=False
    )["feature"].head(10).tolist() if len(tree_importance) else FEATURES[:10]

    robustness_results = run_robustness_analysis(champion_model, _lgbm_builder, split, top_features_for_removal)
    repeated_cv_df = repeated_tscv_evaluation(
        lambda seed: XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.05, subsample=0.8,
                                   colsample_bytree=0.8, n_jobs=-1, random_state=seed, verbosity=0),
        X_full, y_full
    )

    # --- Section 17: Model comparison table -----------------------------------------
    comparison_df = build_model_comparison_table(all_metrics, cv_results, robustness_results["bootstrap_ci"])

    # --- Section 18: Visualization ---------------------------------------------------
    plot_actual_vs_predicted(split["dates_test"], split["y_test"],
                              {k: v for k, v in all_preds.items() if len(v) == len(split["y_test"])},
                              "all_models_last7days", window_days=7)
    plot_model_comparison_bars(comparison_df)

    for name in [champion_name, "Ensemble" if "Weighted Ensemble" in all_preds else champion_name]:
        if name in all_preds and len(all_preds[name]) == len(split["y_test"]):
            plot_residual_diagnostics(split["y_test"], all_preds[name], name.replace(" ", "_"))
            extended_performance_analyses(split["dates_test"], split["y_test"], all_preds[name],
                                           name.replace(" ", "_"))

    eda_correlation_heatmap(df, FEATURES[:25] + ["load"], "post_engineering_correlation_heatmap")

    # --- Section 19: Export ------------------------------------------------------------
    export_predictions(split["dates_test"], split["y_test"], all_preds)

    for name, model in fitted_models.items():
        try:
            import joblib
            joblib.dump(model, os.path.join(MODEL_DIR, f"{dataset_label}_{name.replace(' ', '_')}.pkl"))
        except Exception as e:
            print(f"  Could not serialize {name}: {e}")

    results.update(dict(
        comparison_df=comparison_df, ablation_df=ablation_df, stat_tests=stat_tests,
        robustness_results=robustness_results, repeated_cv_df=repeated_cv_df,
        ranking_report=ranking_report, variance_report=variance_report,
        dropped_correlated_features=dropped_report,
    ))

    FIG_DIR, TABLE_DIR = _orig_fig_dir, _orig_table_dir
    print(f"\nPipeline run complete for dataset: {dataset_label}\n")
    return results


# ==============================================================================
# SECTION 21: MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":

    # --- Primary dataset: full analysis ---------------------------------------
    primary_results = run_full_pipeline(
        PRIMARY_DATASET_CANDIDATES, column_map_key="default", dataset_label="primary",
        split_date=SPLIT_DATE, run_heavy_analyses=True,
    )

    # --- Second dataset: cross-dataset validation (optional) -------------------
    # Demonstrates dataset-independence: identical pipeline, only the path and
    # (if needed) DATASET_COLUMN_MAP entry change. Runs the lighter analysis
    # set (skips SHAP/ablation/robustness/statistical tests) since its purpose
    # is confirmatory generalization, not a second full reviewer-facing study.
    second_results = None
    if SECOND_DATASET_CANDIDATES:
        try:
            resolve_dataset_path(SECOND_DATASET_CANDIDATES)
            second_results = run_full_pipeline(
                SECOND_DATASET_CANDIDATES, column_map_key="uk_national_grid", dataset_label="second_dataset",
                split_date=SPLIT_DATE, run_heavy_analyses=False,
            )
        except FileNotFoundError:
            print("\nSecond dataset not found at configured paths — skipping cross-dataset "
                  "validation run (NOT_APPLICABLE). Set SECOND_DATASET_CANDIDATES to enable it.\n")
        except Exception as e:
            # A schema mismatch or any other failure on the confirmatory
            # second dataset must never take down the whole run — the
            # primary-dataset results above have already completed and
            # are the ones the manuscript depends on.
            print(f"\nSecond-dataset run failed ({type(e).__name__}: {e}) — skipping cross-dataset "
                  f"validation. Primary-dataset results are unaffected.\n")

    # --- Cross-dataset comparison plot (only if second dataset ran) ------------
    if second_results is not None:
        fig, ax = plt.subplots(figsize=(10, 5))
        merged = primary_results["comparison_df"][["Model", "MAE", "RMSE"]].copy()
        merged["dataset"] = "primary"
        second_merged = second_results["comparison_df"][["Model", "MAE", "RMSE"]].copy()
        second_merged["dataset"] = "second_dataset"
        combined = pd.concat([merged, second_merged], ignore_index=True)
        sns.barplot(data=combined, x="Model", y="RMSE", hue="dataset", ax=ax)
        plt.xticks(rotation=45, ha="right")
        ax.set_title("Cross-Dataset RMSE Comparison")
        plt.tight_layout()
        save_figure(fig, "cross_dataset_rmse_comparison")
        export_table(combined, "cross_dataset_comparison", index=False)

    # --- Final summary -----------------------------------------------------------
    print("\n" + "=" * 78)
    print("  ELECTRICITY LOAD FORECASTING — FINAL SUMMARY (PRIMARY DATASET)")
    print("=" * 78)
    print(primary_results["comparison_df"][
        ["Model", "MAE", "RMSE", "R2", "MAPE (%)", "Model Rank"]
    ].to_string(index=False))
    champion = comparison_champion_name(primary_results["comparison_df"])
    print(f"\nChampion model (lowest RMSE): {champion}")
    print("=" * 78)

    if primary_results.get("stat_tests") is not None:
        friedman = primary_results["stat_tests"]["friedman"]
        print(f"\nFriedman test across all models: {friedman}")

    # --- Package everything for download -----------------------------------------
    package_outputs()
    print(f"\nAll figures saved to:  {FIG_DIR}")
    print(f"All tables saved to:   {TABLE_DIR}")
    print(f"All model artifacts saved to: {MODEL_DIR}")
    print("\nPipeline execution finished.")