import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error,
    accuracy_score,
    precision_score,
    recall_score,
    classification_report
)

def load_data():
    vix = yf.download("^VIX", start="2010-01-01")
    spy = yf.download("SPY", start="2010-01-01")

    df = pd.DataFrame()
    df["VIX"] = vix["Close"]
    df["SPY"] = spy["Close"]

    return df.dropna()


# Features
def create_features(df):
    df = df.copy()

    # Returns
    df["VIX_return"] = df["VIX"].pct_change()
    df["SPY_return"] = df["SPY"].pct_change()

    # Rolling features
    df["VIX_ma_5"] = df["VIX"].rolling(5).mean()
    df["VIX_ma_10"] = df["VIX"].rolling(10).mean()
    df["VIX_std_10"] = df["VIX"].rolling(10).std()

    # Lag features
    df["VIX_lag1"] = df["VIX"].shift(1)
    df["VIX_lag2"] = df["VIX"].shift(2)

    # next day VIX
    df["target_reg"] = df["VIX"].shift(-1)

    # Classification target (VIX spike > 5%)
    df["target_cls"] = (df["target_reg"] / df["VIX"] - 1 > 0.05).astype(int)

    return df.dropna()

# Train
def train_models(df):
    features = [
        "VIX_return", "SPY_return",
        "VIX_ma_5", "VIX_ma_10", "VIX_std_10",
        "VIX_lag1", "VIX_lag2"
    ]

    X = df[features]

    y_reg = df["target_reg"]

    y_cls = df["target_cls"]

    X_train, X_test, y_reg_train, y_reg_test, y_cls_train, y_cls_test = train_test_split(
        X, y_reg, y_cls, shuffle=False, test_size=0.2
    )

    # Regression Models
    lr = LinearRegression()
    rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)

    lr.fit(X_train, y_reg_train)
    rf_reg.fit(X_train, y_reg_train)

    lr_pred = lr.predict(X_test)
    rf_pred = rf_reg.predict(X_test)

    print("\n--- Regression ---")
    print("Linear Regression RMSE:", np.sqrt(mean_squared_error(y_reg_test, lr_pred)))
    print("Random Forest RMSE:", np.sqrt(mean_squared_error(y_reg_test, rf_pred)))

    log = LogisticRegression(max_iter=1000)
    rf_cls = RandomForestClassifier(n_estimators=100, random_state=42)

    log.fit(X_train, y_cls_train)
    rf_cls.fit(X_train, y_cls_train)

    log_pred = log.predict(X_test)
    rf_cls_pred = rf_cls.predict(X_test)

    print("\n--- Classification ---")
    print("Logistic Regression Accuracy:", accuracy_score(y_cls_test, log_pred))
    print("Random Forest Accuracy:", accuracy_score(y_cls_test, rf_cls_pred))

    print("\nRandom Forest Classification Report:")
    print(classification_report(y_cls_test, rf_cls_pred))

    return lr, rf_reg, log, rf_cls

if __name__ == "__main__":
    df = load_data()
    df = create_features(df)
    train_models(df)