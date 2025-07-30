import cv2
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.cluster import KMeans
from collections import Counter

gender_model = load_model('gender_model.h5')
glasses_model = load_model('glasses_model.h5')


def preprocess_image(image_path, target_size=(128, 128)):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not loaded from path: {image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def predict_features(image_path):
    img_array = preprocess_image(image_path)
    gender_pred = gender_model.predict(img_array)[0]
    gender = 'Male' if gender_pred[0] > 0.7 else 'Female'

    glasses_pred = glasses_model.predict(img_array)[0]
    glasses = 'Wearing Glasses' if glasses_pred[0] > 0.5 else 'No Glasses'

    return f"{gender}, {glasses}"


def crop_shirt_area(img):
    height, width, _ = img.shape
    top = int(height * 0.4)
    bottom = int(height * 0.75)
    left = int(width * 0.25)
    right = int(width * 0.75)
    return img[top:bottom, left:right]


def get_dominant_color(image_path, k=3):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found.")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    shirt_region = crop_shirt_area(img)
    pixels = shirt_region.reshape((-1, 3))
    pixels = pixels[np.any(pixels != [255, 255, 255], axis=1)]  

    if len(pixels) == 0:
        return "Unknown"

    kmeans = KMeans(n_clusters=k, n_init='auto')
    kmeans.fit(pixels)
    counts = Counter(kmeans.labels_)
    center_color = kmeans.cluster_centers_[counts.most_common(1)[0][0]]
    return f"RGB({int(center_color[0])}, {int(center_color[1])}, {int(center_color[2])})"
