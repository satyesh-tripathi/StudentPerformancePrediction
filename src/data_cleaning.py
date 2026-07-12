import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = Path("Dataset/student-mat.csv")
CLEAN_PATH = Path("Dataset/student_mat_cleaned.csv")

LEAKAGE_COLS = ["G1", "G2"]
BINARY_COLS = ["schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic"]
BINARY_OTHER = {
    "school": {"GP": 1, "MS": 0},
    "sex": {"F": 1, "M": 0},
    "address": {"U": 1, "R": 0},
    "famsize": {"GT3": 1, "LE3": 0},
    "Pstatus": {"T": 1, "A": 0}
}
NOMINAL_COLS = ["Mjob", "Fjob", "reason", "guardian"]

def clean():
    df = pd.read_csv(RAW_PATH, sep=";")
    
    # Outlier treatment for absences
    q1, q3 = df["absences"].quantile([0.25, 0.75])
    upper_bound = q3 + 1.5 * (q3 - q1)
    df["absences"] = df["absences"].clip(upper=upper_bound)
    
    # Target Leakage Drop
    df = df.drop(columns=LEAKAGE_COLS, errors="ignore")
    
    # Mappings
    for col in BINARY_COLS:
        df[col] = df[col].map({"yes": 1, "no": 0})
        
    rename_map = {"school": "school_GP", "sex": "sex_F", "address": "address_urban", "famsize": "famsize_GT3", "Pstatus": "Pstatus_together"}
    for col, mapping in BINARY_OTHER.items():
        df[col] = df[col].map(mapping)
    df = df.rename(columns=rename_map)
    
    df = pd.get_dummies(df, columns=NOMINAL_COLS, drop_first=True)
    
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)
    print(f"Phase 4 Complete: Cleaned file generated at {CLEAN_PATH} with shape {df.shape}")

if __name__ == "__main__":
    clean()