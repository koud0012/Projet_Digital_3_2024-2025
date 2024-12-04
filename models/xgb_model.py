# from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Import the sys library to redirect output
import sys

from datetime import datetime

# Get the current time
run_time = datetime.now().strftime("%H:%M:%S")

print(f"Run time : {run_time}")

train_data = pd.read_csv('../data/data_essentials_ecobalyse_train.csv') 


X_train = train_data[['product', 'mass_kg', 'material_id', 'countryMaking']]
y_train = train_data['impact_ecs']


# Preprocessing categorical variables
categorical_features = ['product', 'material_id', 'countryMaking']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

n_estimator = 1000

# Create and train the XGBRegressor model with pipeline
xgb_model = XGBRegressor(
    n_estimators=n_estimator,
    max_depth=4,
    learning_rate=0.01,
    verbosity=1  # 1 or 2 to have information on progress
)

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', xgb_model)
])


# Fit the model with cross-validation
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
mean_cv_score = -np.mean(cv_scores)

# Final training
pipeline.fit(X_train, y_train)

pkl_filename = f'pkl_models/xgb_model_{n_estimator}.pkl'

# Save the trained model
joblib.dump(pipeline, pkl_filename)

# Predict on training data
predictions = pipeline.predict(X_train)

# Add predictions to the training DataFrame
train_data['predicted_impact_ecs'] = predictions
print(train_data[['impact_ecs', 'predicted_impact_ecs']].head())

# Calculate evaluation metrics
rmse_rf = round(np.sqrt(mean_squared_error(y_train, predictions)), 4)
mae_rf = round(mean_absolute_error(y_train, predictions), 4)
errors = y_train - predictions

# Calculate the variance of the errors
variance_errors = round(np.var(errors), 4)

# Calculate the standard deviation of the errors
sd_errors = round(np.std(errors), 4)

# Calculate the mean of the errors
mean_error = np.mean(errors)

# Calculate the mean of the actual values to express the error in percentage
mean_real = np.mean(y_train)

# Define the interval in percentage (e.g., ±1 standard deviation)
interval_low = round((mean_error - sd_errors) / mean_real * 100, 4)
interval_high = round((mean_error + sd_errors) / mean_real * 100, 4)

# Display results
print(f"Average error interval in percentage: [{interval_low}% , {interval_high}%]")
print(f"Variance of the error: {variance_errors}")
print(f"Standard deviation of the error: {sd_errors}")

# Calculate R²
ss_total = np.sum((y_train - np.mean(y_train)) ** 2)
ss_residual = np.sum((y_train - predictions) ** 2)
r_squared_rf = round(1 - (ss_residual / ss_total), 4)

# Calculate MAPE
mape_rf = round(np.mean(np.abs((y_train - predictions) / y_train)) * 100, 4)

# Display results
print("Model performance on training data using XGBoosting model:")
print(f"MAPE (percentage error): {mape_rf}%")
print(f"RMSE: {rmse_rf}")
print(f"MAE: {mae_rf}")
print(f"R²: {r_squared_rf}")

print(f"Number of rows in the training data: {train_data.shape[0]}")

# Open a file for writing
txt_filename = f"performance/train/train_data_performance_xgb_model_{n_estimator}.txt"
with open(txt_filename, 'w') as f:
    # Redirect standard output to the file
    original_stdout = sys.stdout
    sys.stdout = f

    # Add predictions to the training DataFrame
    train_data['predicted_impact_ecs'] = predictions
    print(train_data[['impact_ecs', 'predicted_impact_ecs']].head())

    # Display evaluation metrics results
    print(f"Average error interval in percentage: [{interval_low}% , {interval_high}%]")
    print(f"Variance of the error: {variance_errors}")
    print(f"Standard deviation of the error: {sd_errors}")

    print("Model performance on training data using XGBoosting model:")
    print(f"MAPE (percentage error): {mape_rf}%")
    print(f"RMSE: {rmse_rf}")
    print(f"MAE: {mae_rf}")
    print(f"R²: {r_squared_rf}")

    print(f"Number of rows in the training data: {train_data.shape[0]}")

# Restore standard output
sys.stdout = original_stdout

# Get the current time
end_time = datetime.now().strftime("%H:%M:%S")

print(f"End time : {end_time}")