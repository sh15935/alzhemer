import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import json
from .clinical_rules import apply_clinical_rules

# Global model variable
model = None
CLASS_LABELS = ['NonDemented', 'VeryMildDemented', 'MildDemented', 'ModerateDemented']

def load_model(model_path):
    global model
    try:
        model = tf.keras.models.load_model(model_path)
        print(f"Model loaded successfully from {model_path}")
    except Exception as e:
        print(f"Failed to load model: {e}")
        model = None

def predict_image(filepath):
    if model is None:
        return None
    try:
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        prediction = model.predict(img_array)
        return prediction[0]  # Return just the prediction array
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

def comprehensive_assessment(image_prediction, clinical_data):
    """
    Combine image-based prediction with clinical data for comprehensive assessment
    """
    # Get image-based prediction
    img_pred_idx = np.argmax(image_prediction)
    img_confidence = float(image_prediction[img_pred_idx])
    img_label = CLASS_LABELS[img_pred_idx]

    # Apply clinical rules
    clinical_result = apply_clinical_rules(clinical_data)
    clinical_risk = clinical_result["risk_score"]

    # Combine predictions (simple weighted average for demo)
    final_confidence = (img_confidence * 0.7) + (clinical_risk * 0.3)

    # Adjust prediction based on clinical factors
    if clinical_risk > 0.7 and img_confidence < 0.6:
        # High clinical risk outweighs uncertain image prediction
        final_prediction = "High Risk - Clinical factors dominant"
    else:
        final_prediction = img_label

    return {
        "image_prediction": {
            "label": img_label,
            "confidence": img_confidence,
            "probabilities": {label: float(prob) for label, prob in zip(CLASS_LABELS, image_prediction)}
        },
        "clinical_risk_score": clinical_risk,
        "clinical_factors": clinical_result["risk_factors"],
        "final_assessment": final_prediction,
        "final_confidence": final_confidence
    }