import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ---------------------------------------------------------------------------
# Load dataset
# ---------------------------------------------------------------------------
data = pd.read_csv("house_prices_city_dataset.csv")

NUMERIC_FEATURES = ["area", "bedrooms", "bathrooms", "stories", "parking"]
CATEGORICAL_FEATURES = ["country", "location_type"]

X = data[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
y = data["price"]


# ---------------------------------------------------------------------------
# Split data
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ---------------------------------------------------------------------------
# Build a pipeline: one-hot encode country + location_type, pass numeric
# columns through untouched, then feed everything into LinearRegression.
#
# Saving the whole pipeline (not just the bare model) means views.py can
# hand it raw values like "India" / "Metropolitan" directly at predict
# time — no separate multiplier step needed anymore.
# ---------------------------------------------------------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
    ],
    remainder="passthrough",  # numeric columns pass through as-is
)

model = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("regressor", LinearRegression()),
])


# ---------------------------------------------------------------------------
# Train
# ---------------------------------------------------------------------------
model.fit(X_train, y_train)


# ---------------------------------------------------------------------------
# Evaluate
# ---------------------------------------------------------------------------
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model trained successfully!")
print("MAE:", mae)
print("MSE:", mse)
print("R2 Score:", r2)


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
joblib.dump(model, "house_price_model.pkl")
print("Model saved successfully!")