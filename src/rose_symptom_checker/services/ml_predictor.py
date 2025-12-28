import joblib
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class MLPredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.symptom_features = None
        self._load_models()
    
    def _load_models(self):
        try:
            model_path = Path(__file__).parent.parent / "ml" / "model.pkl"
            encoder_path = Path(__file__).parent.parent / "ml" / "label_encoder.pkl"
            
            if model_path.exists():
                self.model = joblib.load(model_path)
                logger.info("ML model loaded successfully")
            else:
                logger.warning("ML model not found. Please train the model first.")
            
            if encoder_path.exists():
                self.label_encoder = joblib.load(encoder_path)
                logger.info("Label encoder loaded successfully")
            else:
                logger.warning("Label encoder not found")
            
            # Define all possible symptoms (features)
            self.symptom_features = [
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
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.model = None
            self.label_encoder = None
    
    def predict(self, symptoms: List[str]) -> Tuple[str, float]:
        if self.model is None or self.label_encoder is None:
            # Fallback prediction if model not loaded
            return self._rule_based_prediction(symptoms)
        
        try:
            # Create feature vector
            feature_vector = self._symptoms_to_features(symptoms)
            
            # Predict
            prediction = self.model.predict([feature_vector])[0]
            probabilities = self.model.predict_proba([feature_vector])[0]
            
            # Get disease name and confidence
            disease = self.label_encoder.inverse_transform([prediction])[0]
            confidence = float(max(probabilities))
            
            return disease, confidence
        
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return self._rule_based_prediction(symptoms)
    
    def _symptoms_to_features(self, symptoms: List[str]) -> List[int]:
        """Convert symptom list to binary feature vector"""
        return [1 if symptom in symptoms else 0 for symptom in self.symptom_features]
    
    def _rule_based_prediction(self, symptoms: List[str]) -> Tuple[str, float]:
        """Simple rule-based prediction as fallback"""
        symptom_set = set(symptoms)
        
        # Black Spot
        if {"dark_spots_on_leaves", "yellowing_leaves", "leaf_drop"}.intersection(symptom_set):
            return "Black Spot", 0.85
        
        # Powdery Mildew
        if {"white_powdery_coating", "distorted_leaves"}.intersection(symptom_set):
            return "Powdery Mildew", 0.80
        
        # Rust
        if {"orange_rust_spots", "leaf_underside_pustules"}.intersection(symptom_set):
            return "Rust", 0.82
        
        # Botrytis Blight
        if {"gray_mold_on_flowers", "brown_spots_on_petals"}.intersection(symptom_set):
            return "Botrytis Blight", 0.78
        
        # Rose Mosaic
        if {"yellow_mosaic_pattern", "vein_clearing"}.intersection(symptom_set):
            return "Rose Mosaic Virus", 0.75
        
        # Crown Gall
        if {"tumor_like_growths", "swollen_stems"}.intersection(symptom_set):
            return "Crown Gall", 0.80
        
        return "Healthy", 0.90
    
    def get_recommendations(self, disease: str) -> List[str]:
        """Get treatment recommendations for diagnosed disease"""
        recommendations_db: Dict[str, List[str]] = {
            "Black Spot": [
                "Remove and destroy infected leaves immediately",
                "Apply fungicide every 7-14 days during wet weather",
                "Improve air circulation by pruning",
                "Water at the base of the plant, avoid wetting foliage",
                "Apply mulch to prevent soil splash"
            ],
            "Powdery Mildew": [
                "Spray with neem oil or sulfur-based fungicide",
                "Increase air circulation and reduce humidity",
                "Remove infected plant parts",
                "Avoid overhead watering",
                "Apply fungicide at first sign of disease"
            ],
            "Rust": [
                "Remove infected leaves and debris",
                "Apply fungicide containing myclobutanil",
                "Improve air circulation",
                "Avoid overhead watering",
                "Plant rust-resistant varieties"
            ],
            "Botrytis Blight": [
                "Remove dead flowers and infected tissue",
                "Improve air circulation",
                "Reduce humidity around plants",
                "Apply appropriate fungicide",
                "Avoid overcrowding plants"
            ],
            "Rose Mosaic Virus": [
                "No cure available - manage symptoms",
                "Maintain plant vigor with proper care",
                "Use virus-free planting material",
                "Control aphid populations",
                "Remove severely infected plants"
            ],
            "Crown Gall": [
                "Remove and destroy infected plants",
                "Disinfect pruning tools between cuts",
                "Avoid wounding plants",
                "Improve soil drainage",
                "Use disease-free planting stock"
            ],
            "Healthy": [
                "Continue regular maintenance",
                "Monitor for early signs of disease",
                "Maintain proper watering schedule",
                "Fertilize according to plant needs",
                "Practice good garden hygiene"
            ]
        }
        
        return recommendations_db.get(disease, ["Consult with a local horticulturist"])


# Global predictor instance
predictor = MLPredictor()