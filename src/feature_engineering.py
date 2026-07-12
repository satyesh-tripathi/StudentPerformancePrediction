import pandas as pd
from pathlib import Path

CLEANED_PATH = Path("Dataset/student_mat_cleaned.csv")
FEATURES_PATH = Path("Dataset/student_mat_features.csv")

DROP_LOW_IMPORTANCE = [
    "paid", "address_urban", "reason_home", "school_GP", "nursery",
    "Pstatus_together", "Fjob_services", "Mjob_teacher", "reason_other", "Fjob_health"
]

def run():
    df = pd.read_csv(CLEANED_PATH)
    
    # Build parental index feature
    df["parental_edu_avg"] = (df["Medu"] + df["Fedu"]) / 2.0
    df = df.drop(columns=["Medu", "Fedu"])
    
    # Isolate key dimensions
    df = df.drop(columns=[c for c in DROP_LOW_IMPORTANCE if c in df.columns], errors="ignore")
    
    FEATURES_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEATURES_PATH, index=False)
    print(f"Phase 6 Complete: Features generated at {FEATURES_PATH} with shape {df.shape}")

if __name__ == "__main__":
    run()