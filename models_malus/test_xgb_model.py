import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
from sklearn.model_selection import train_test_split

import sys


# Load the test dataset
test_data = pd.read_csv('./data/transformed_data_difference_simple_multi_test.csv')


features = ['product_encoded', 'material_id_1_encoded', 'material_share_1', 'nb_materiaux']
target = 'malus_per_mass_kg'


X_test = test_data[features]
y_test = test_data[target]

n_estimator = 10000
depth = 6

pkl_filename = f'pkl_models/xgb_model_{n_estimator}_depth_{depth}.pkl'
# Load the trained model
pipeline = joblib.load(pkl_filename)

# Predict on the test data
predictions = pipeline.predict(X_test)


# Add predictions to the training DataFrame
test_data[f'predicted_{target}'] = predictions
print(test_data[[target, f'predicted_{target}']].head(10))

# Calculate evaluation metrics
rmse_rf = round(np.sqrt(mean_squared_error(y_test, predictions)), 4)
mae_rf = round(mean_absolute_error(y_test, predictions), 4)
errors = y_test - predictions

# Calculate the variance of the errors
variance_errors = round(np.var(errors), 4)

# Calculate the standard deviation of the errors
sd_errors = round(np.std(errors), 4)

# Calculate the mean of the errors
mean_error = np.mean(errors)

# Calculate the mean of the actual values to express the error in percentage
mean_real = np.mean(y_test)

# Define the interval in percentage (e.g., ±1 standard deviation)
interval_low = round((mean_error - sd_errors) / mean_real * 100, 4)
interval_high = round((mean_error + sd_errors) / mean_real * 100, 4)

# Display results
print(f"Average error interval in percentage: [{interval_low}% , {interval_high}%]")
print(f"Variance of the error: {variance_errors}")
print(f"Standard deviation of the error: {sd_errors}")

# Calculate R²
ss_total = round(np.sum((y_test - np.mean(y_test)) ** 2), 4)
ss_residual =round(np.sum((y_test - predictions) ** 2), 4)
r_squared_rf =round(1 - (ss_residual / ss_total), 4)

# Calculate MAPE
mape_rf = round(np.mean(np.abs((y_test - predictions) / y_test)) * 100, 4)

# Display results
print("Model performance on test data using XGBoosting model:")
print(f"MAPE (percentage error): {mape_rf}%")
print(f"RMSE: {rmse_rf}")
print(f"MAE: {mae_rf}")
print(f"R²: {r_squared_rf}")

print(f"Number of rows in the test data: {test_data.shape[0]}")

# Open a file for writing
txt_filename = f"performance/test/test_data_performance_xgb_model_{n_estimator}.txt"
with open(txt_filename, 'w') as f:
    # Redirect standard output to the file
    original_stdout = sys.stdout
    sys.stdout = f

    # Add predictions to the training DataFrame
    test_data[f'predicted_{target}'] = predictions
    print(test_data[[target, f'predicted_{target}']].head())

    # Display results
    print(f"Average error interval in percentage: [{interval_low}% , {interval_high}%]")
    print(f"Variance of the error: {variance_errors}")
    print(f"Standard deviation of the error: {sd_errors}")

    # Display results
    print("Model performance on test data using XGBoosting model:")
    print(f"MAPE (percentage error): {mape_rf}%")
    print(f"RMSE: {rmse_rf}")
    print(f"MAE: {mae_rf}")
    print(f"R²: {r_squared_rf}")

    print(f"Number of rows in the test data: {test_data.shape[0]}")

# Restore standard output
sys.stdout = original_stdout

