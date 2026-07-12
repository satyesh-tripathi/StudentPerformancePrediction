streamlit run Streamlit_App/app.pyimport pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb

FEATURES_PATH = Path("Dataset/student_mat_features.csv")
MODEL_PATH = Path("Model/student_performance_best_model.pkl")

def tune():
    df = pd.read_csv(FEATURES_PATH)
    X = df.drop(columns=["G3"])
    y = df["G3"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    xgb_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('xgb', xgb.XGBRegressor(random_state=42, objective='reg:squarederror'))
    ])

    xgb_param_grid = {
        'xgb__n_estimators': [50, 100, 150],
        'xgb__learning_rate': [0.01, 0.05, 0.1],
        'xgb__max_depth': [3, 4, 5],
        'xgb__subsample': [0.8, 1.0]
    }

    grid = GridSearchCV(xgb_pipeline, xgb_param_grid, cv=5, scoring='neg_root_mean_squared_error', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    best_pipeline = grid.best_estimator_
    y_pred = best_pipeline.predict(X_test)
    
    print(f"Optimized Parameters: {grid.best_params_}")
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
    print(f"R2 Score: {r2_score(y_test, y_pred):.4f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipeline, MODEL_PATH)
    print(f"Model Engine persisted successfully at {MODEL_PATH}")

if __name__ == "__main__":
    tune()	