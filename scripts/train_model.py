import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)


def create_synthetic_dataset(n_samples=1000):
    """
    Create a synthetic dataset for rose disease classification
    """
    diseases = [
        "Black Spot",
        "Powdery Mildew",
        "Rust",
        "Botrytis Blight",
        "Rose Mosaic Virus",
        "Crown Gall",
        "Healthy"
    ]
    
    # Define symptom features
    symptoms = [
        "dark_spots_on_leaves",
        "yellowing_leaves",
        "leaf_drop",
        "white_powdery_coating",
        "distorted_leaves",
        "stunted_growth",
        "orange_rust_spots",
        "leaf_underside_pustules",
        "premature_leaf_fall",
        "gray_mold_on_flowers",
        "brown_spots_on_petals",
        "flower_rot",
        "yellow_mosaic_pattern",
        "vein_clearing",
        "reduced_flowering",
        "tumor_like_growths",
        "swollen_stems",
        "wilting",
        "holes_in_leaves",
        "webbing_on_leaves"
    ]
    
    # Disease-symptom relationships (probability of symptom given disease)
    disease_symptom_map = {
        "Black Spot": {
            "dark_spots_on_leaves": 0.95,
            "yellowing_leaves": 0.85,
            "leaf_drop": 0.80,
            "premature_leaf_fall": 0.70
        },
        "Powdery Mildew": {
            "white_powdery_coating": 0.95,
            "distorted_leaves": 0.75,
            "stunted_growth": 0.65,
            "reduced_flowering": 0.60
        },
        "Rust": {
            "orange_rust_spots": 0.95,
            "leaf_underside_pustules": 0.90,
            "yellowing_leaves": 0.70,
            "premature_leaf_fall": 0.75
        },
        "Botrytis Blight": {
            "gray_mold_on_flowers": 0.95,
            "brown_spots_on_petals": 0.90,
            "flower_rot": 0.85,
            "wilting": 0.60
        },
        "Rose Mosaic Virus": {
            "yellow_mosaic_pattern": 0.95,
            "vein_clearing": 0.85,
            "reduced_flowering": 0.70,
            "stunted_growth": 0.65
        },
        "Crown Gall": {
            "tumor_like_growths": 0.95,
            "swollen_stems": 0.90,
            "stunted_growth": 0.75,
            "wilting": 0.60
        },
        "Healthy": {
            # Healthy plants might have very mild symptoms occasionally
            "holes_in_leaves": 0.10,
            "webbing_on_leaves": 0.05
        }
    }
    
    data = []
    
    for _ in range(n_samples):
        # Randomly select a disease
        disease = np.random.choice(diseases)
        
        # Create symptom vector based on disease
        symptom_vector = []
        for symptom in symptoms:
            prob = disease_symptom_map.get(disease, {}).get(symptom, 0.05)
            # Add some noise
            prob = min(max(prob + np.random.normal(0, 0.1), 0), 1)
            symptom_vector.append(1 if np.random.random() < prob else 0)
        
        data.append(symptom_vector + [disease])
    
    # Create DataFrame
    columns = symptoms + ["disease"]
    df = pd.DataFrame(data, columns=columns)
    
    return df, symptoms


def train_model():
    """
    Train the rose disease classification model
    """
    print("Creating synthetic dataset...")
    df, symptom_features = create_synthetic_dataset(n_samples=2000)
    
    print(f"Dataset created with {len(df)} samples")
    print(f"\nDisease distribution:")
    print(df['disease'].value_counts())
    
    # Prepare features and labels
    X = df[symptom_features].values
    y = df['disease'].values
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Train Random Forest model
    print("\nTraining Random Forest classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=label_encoder.classes_
    ))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': symptom_features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Important Features:")
    print(feature_importance.head(10))
    
    # Save model and encoder
    model_dir = Path(__file__).parent.parent / "src" / "ml"
    model_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = model_dir / "model.pkl"
    encoder_path = model_dir / "label_encoder.pkl"
    
    joblib.dump(model, model_path)
    joblib.dump(label_encoder, encoder_path)
    
    print(f"\nModel saved to: {model_path}")
    print(f"Label encoder saved to: {encoder_path}")
    
    # Save training data for reference
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(data_dir / "rose_diseases.csv", index=False)
    print(f"Training data saved to: {data_dir / 'rose_diseases.csv'}")


if __name__ == "__main__":
    train_model()