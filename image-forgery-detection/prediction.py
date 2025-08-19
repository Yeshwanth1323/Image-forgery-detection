import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps

# Load trained model once
model = load_model('trained_model.h5')

# Constants
IMG_SIZE = (128, 128)
CLASS_NAMES = ['Authentic', 'Tampered']

def prepare_image(image_path):
    """
    Load and preprocess the image for prediction.
    Converts image to RGB, resizes, normalizes, and reshapes it.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img = ImageOps.exif_transpose(img)  # Handle image rotation
        img = img.resize(IMG_SIZE)
        img_array = np.array(img) / 255.0  # Normalize to [0, 1]
        if img_array.shape != (128, 128, 3):
            raise ValueError("Image shape is invalid after resizing.")
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        return img_array
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")

def predict_ela_image(image_array):
    """
    Predicts authenticity using the model.
    Returns both label and confidence score.
    """
    try:
        prediction = model.predict(image_array)
        class_idx = int(np.argmax(prediction))
        confidence = float(np.max(prediction)) * 100
        label = CLASS_NAMES[class_idx]
        return f"{label} (Confidence: {confidence:.2f}%)"
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {e}")