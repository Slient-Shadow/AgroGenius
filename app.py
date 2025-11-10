from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Conv2DTranspose
from PIL import Image
import io
import os
import cv2
from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Conv2DTranspose
from PIL import Image
import io
import os
import cv2

app = Flask(__name__)

MODEL_PATH = os.path.join("model", "unet_model.h5")

# --- 🔧 Compatibility Fix for Older TensorFlow Versions ---
# Some TF builds don't support `groups` argument in Conv2DTranspose.
# This patch removes unexpected kwargs before layer creation.
import inspect

old_init = Conv2DTranspose.__init__

def safe_init(self, *args, **kwargs):
    if "groups" in kwargs:
        kwargs.pop("groups")
    try:
        old_init(self, *args, **kwargs)
    except TypeError:
        # silently ignore unknown args in older TF builds
        valid_args = inspect.signature(old_init).parameters
        filtered = {k: v for k, v in kwargs.items() if k in valid_args}
        old_init(self, *args, **filtered)

Conv2DTranspose.__init__ = safe_init
# ------------------------------------------------------------

model = load_model(MODEL_PATH, compile=False)
print("✅ Model loaded successfully!")

# Image preprocessing function
def preprocess_image(image):
    image = image.resize((128, 128))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files.get('image')
        if file is None:
            return jsonify({"error": "No file uploaded"}), 400

        # Read image from request
        image = Image.open(io.BytesIO(file.read())).convert("RGB")
        img = np.array(image)

        # Resize & normalize
        img = cv2.resize(img, (128, 128))
        img = img / 255.0

        # Model prediction
        prediction = model.predict(np.expand_dims(img, axis=0))  # shape: (1,128,128,1)

        # Thresholding
        threshold = 0.2
        binary_prediction = (prediction > threshold).astype(np.uint8)

        # Seed quality score
        seed_quality_score = np.sum(binary_prediction) / (128 * 128)

        # Apply your Tkinter logic
        if seed_quality_score >= 0.2:
            quality_msg = "Seed is Not Suitable for Farming"
        else:
            quality_msg = "Seed is Good for Farming"

        return jsonify({
            "quality": quality_msg,
            "defect_fraction": float(seed_quality_score)
        })

    except Exception as e:
        print("❌ SERVER ERROR:", str(e))
        return jsonify({"error": "Server crashed", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
