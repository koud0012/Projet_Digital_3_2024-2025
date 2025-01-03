# Import necessary libraries
from xgboost import XGBRegressor, plot_importance
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
import joblib
import matplotlib.pyplot as plt


from datetime import datetime

# Record the start time
run_time = datetime.now().strftime("%H:%M:%S")
print(f"Run time : {run_time}")

# Load training and test data
train_data = pd.read_csv('./data/transformed_data_difference_simple_multi_train.csv')
test_data = pd.read_csv('./data/transformed_data_difference_simple_multi_test.csv')

# Define features and target
features = ['product', 'material_id', 'material_share', 'nb_materiaux']
target = 'malus_per_mass_kg'

X_train = train_data[features]
y_train = train_data[target]
X_test = test_data[features]
y_test = test_data[target]

# Define hyperparameters
n_estimator = 50000
depth = 5
learning_rate = 0.01

# Create and train the XGBRegressor model with early stopping
xgb_model = XGBRegressor(
    n_estimators=n_estimator,
    max_depth=depth,
    learning_rate=learning_rate,
    verbosity=2,  # 1 ou 2 pour suivre la progression
    early_stopping_rounds=200,  # Arrêt anticipé
    eval_metric="rmse"  # Définition directe de la métrique d'évaluation
)

# Train the model with early stopping
xgb_model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=True
)

# Retrieve the number of estimators used
final_estimators = xgb_model.best_iteration + 1
print(f"Number of estimators used: {final_estimators}")

# Save the trained model
pkl_filename = f'pkl_models/xgb_model_{final_estimators}_depth_{depth}.pkl'
joblib.dump(xgb_model, pkl_filename)

# Predict on training and test data
train_predictions = xgb_model.predict(X_train)
test_predictions = xgb_model.predict(X_test)

# Add predictions to the DataFrames
train_data[f'predicted_{target}'] = train_predictions
test_data[f'predicted_{target}'] = test_predictions

# Display a sample of the predictions
print("train data : ")
print(train_data[[target, f'predicted_{target}']].head(10))
print("test data : ")
print(test_data[[target, f'predicted_{target}']].head(10))



# Calculate evaluation metrics for training data
rmse_train = round(np.sqrt(mean_squared_error(y_train, train_predictions)), 4)
mae_train = round(mean_absolute_error(y_train, train_predictions), 4)
r2_train = round(r2_score(y_train, train_predictions), 4)

# Calculate evaluation metrics for test data
rmse_test = round(np.sqrt(mean_squared_error(y_test, test_predictions)), 4)
mae_test = round(mean_absolute_error(y_test, test_predictions), 4)
r2_test = round(r2_score(y_test, test_predictions), 4)

# Display results
print("Model performance on training data:")
print(f"RMSE: {rmse_train}")
print(f"MAE: {mae_train}")
print(f"R²: {r2_train}")

print("Model performance on test data:")
print(f"RMSE: {rmse_test}")
print(f"MAE: {mae_test}")
print(f"R²: {r2_test}")

# Open a file for writing
txt_filename = f"performance/train_test_performance_xgb_model_{final_estimators}.txt"
with open(txt_filename, 'w') as f:
    # Retrieve the number of estimators used
    final_estimators = xgb_model.best_iteration + 1
    print(f"Number of estimators used: {final_estimators}")

    f.write("Model performance on training data:\n")
    f.write(f"RMSE: {rmse_train}\n")
    f.write(f"MAE: {mae_train}\n")
    f.write(f"R²: {r2_train}\n\n")

    f.write("Model performance on test data:\n")
    f.write(f"RMSE: {rmse_test}\n")
    f.write(f"MAE: {mae_test}\n")
    f.write(f"R²: {r2_test}\n")
    
plt.figure(figsize=(10, 6))
plot_importance(xgb_model, importance_type='weight', title="Feature Importance by Weight")
plt.show()

# Record the end time
end_time = datetime.now().strftime("%H:%M:%S")
print(f"End time : {end_time}")
