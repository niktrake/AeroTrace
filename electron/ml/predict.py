import sys
import os
import math
import joblib
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# ---------- Load Trained Model ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "rf_classifier.pkl")
encoder_path = os.path.join(BASE_DIR, "extension_encoder.pkl")

model = joblib.load(model_path)
le = joblib.load(encoder_path)

# ---------- Feature Functions ----------

def get_first_bytes(file_path, num_bytes=256):

    try:
        with open(file_path, "rb") as f:

            data = f.read(num_bytes)

            # pad if file < 256 bytes
            if len(data) < num_bytes:
                data += bytes([0] * (num_bytes - len(data)))

            return data

    except:
        return None


def compute_entropy(byte_data):

    freq = {}

    for b in byte_data:
        freq[b] = freq.get(b, 0) + 1

    entropy = 0
    length = len(byte_data)

    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)

    return entropy


def compute_null_ratio(byte_data):

    null_count = sum(1 for b in byte_data if b == 0)

    return null_count / len(byte_data)


def compute_ascii_ratio(byte_data):

    ascii_count = sum(1 for b in byte_data if 32 <= b <= 126)

    return ascii_count / len(byte_data)


def get_extension(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    return ext if ext != "" else "unknown"


# ---------- Safe Extension ----------

def safe_extension(ext):

    return ext if ext in le.classes_ else "unknown"


# ---------- Input File ----------

file_path = sys.argv[1]


# ---------- Extract Features ----------

byte_data = get_first_bytes(file_path)

if byte_data is None:
    print("unknown")
    sys.exit()

extension = get_extension(file_path)

# Apply failsafe
extension = safe_extension(extension)

# Encode extension
encoded_extension = le.transform([extension])[0]

# First 10 bytes
first_10 = list(byte_data[:10])

null_ratio = compute_null_ratio(byte_data)

ascii_ratio = compute_ascii_ratio(byte_data)

entropy = compute_entropy(byte_data)


# ---------- Create Feature Vector ----------

features = {
    "extension": encoded_extension
}

# Add byte_0 to byte_9
for i in range(10):
    features[f"byte_{i}"] = first_10[i]

features["null_ratio"] = null_ratio
features["ascii_ratio"] = ascii_ratio
features["entropy"] = entropy

df = pd.DataFrame([features])

# ---------- Predict ----------

prediction = model.predict(df)[0]

# Label Mapping
label_map = {
    1: "cache",
    2: "configuration_file",
    3: "flight_logs",
    4: "image",
    5: "telemetry_logs",
    6: "video"
}

predicted_label = label_map.get(prediction, "unknown")

print(predicted_label)