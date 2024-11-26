import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import json


from scapy.all import sniff, IP, TCP, UDP
packet = []  # Declare as a global variable

def packet_handler(packet_data):
    global packet  # Explicitly declare that we're modifying the global list

    # Extract basic features (expand as per dataset features)
    features_dict = {
        "duration": 1,  # Duration tracking requires session state; set to a default for single packets
        "src_bytes": len(packet_data.payload),
        "dst_bytes": len(packet_data),
        "count": 1,  # Default count per packet
        "srv_count": 1,  # Count of service sessions (single packet)
    }

    # Convert to DataFrame
    packet_df = pd.DataFrame([features_dict])

    # Apply pre-trained scaler
    packet_df_scaled = scaler.transform(packet_df)

    # Predict
    prediction = clf.predict(packet_df_scaled)

    # Append prediction to the global packet list
    packet.append(prediction[0])

    return prediction

def snif():
    sniff(prn=packet_handler, count=10)  # Capture 10 packets for testing
    return packet

















# Step 1: Download dataset using kagglehub
import kagglehub
path = kagglehub.dataset_download("galaxyh/kdd-cup-1999-data")
# print("Path to dataset files:", path)

# List all files in the downloaded dataset
files = os.listdir(path)
# print("Available files:", files)

# Define column names
col_names = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent", "hot",
             "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
             "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", "count", "srv_count",
             "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
             "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
             "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
             "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label"]

# Locate training and test files dynamically
train_file = os.path.join(path, "kddcup.data_10_percent_corrected")
test_file_candidates = [file for file in files if "corrected" in file.lower()]

if not test_file_candidates:
    raise FileNotFoundError("Test file with 'corrected' not found in the dataset directory.")

test_file = os.path.join(path, test_file_candidates[0]) 

file_name = "corrected"
test_file = os.path.join(test_file, file_name)
# print(f"Training file: {train_file}")
# print(f"Test file: {test_file}")

# Step 2: Load training dataset
kdd_data_set = pd.read_csv(train_file, names=col_names)
# print(kdd_data_set.describe())

# Label distribution in training data
# print(kdd_data_set['label'].value_counts())

# Step 3: Select numerical features
num_features = [ "duration",  # Duration tracking requires session state; set to a default for single packets
    "src_bytes",
    "dst_bytes",
    "count" ,  # Default count per packet
    "srv_count"  # Count of service sessions (single packet)
    ]

features = kdd_data_set[num_features].astype(float)
labels_dataset = kdd_data_set['label'].copy()

# Relabel attacks as 'attack.' and normal as 'normal.'
labels_dataset[labels_dataset != 'normal.'] = 'attack.'
# print(labels_dataset.value_counts())

# Step 4: Rescale the features
scaler = MinMaxScaler()
features[:] = scaler.fit_transform(features)
# print(features.describe())

# Step 5: Train the Random Forest Classifier
clf = RandomForestClassifier(random_state=0)
clf.fit(features, labels_dataset)


path = r"C:\Users\Sohail Dil\.cache\kagglehub\datasets\galaxyh\kdd-cup-1999-data\versions\1\corrected"

# Check file existence
folder_path = r"C:\Users\Sohail Dil\.cache\kagglehub\datasets\galaxyh\kdd-cup-1999-data\versions\1\corrected"
subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
# print(subfolders)

# print("test file is",test_file)
test_file = r"C:\Users\Sohail Dil\.cache\kagglehub\datasets\galaxyh\kdd-cup-1999-data\versions\1\corrected\corrected"
try:
    kdd_data_labeled = pd.read_csv(test_file, header=None, names=col_names)
except Exception as e:
    print(f"Error loading test file: {e}")
    raise

# Relabel attacks as 'attack.' and normal as 'normal.'
kdd_data_labeled['label'][kdd_data_labeled['label'] != 'normal.'] = 'attack.'
# print(kdd_data_labeled['label'].value_counts())

# Ensure numerical features are float and scale them
kdd_data_labeled[num_features] = kdd_data_labeled[num_features].astype(float)
kdd_data_labeled[num_features] = scaler.transform(kdd_data_labeled[num_features])

# Step 7: Split into train and test sets
features_train, features_test, labels_train, labels_test = train_test_split(
    kdd_data_labeled[num_features], kdd_data_labeled['label'], test_size=0.1, random_state=42)

# Train classifier on complete training dataset
clf.fit(features_train, labels_train)

# Step 8: Make predictions on the test set
predictions = clf.predict(features_test)

# Step 9: Evaluate accuracy
acc = accuracy_score(predictions, labels_test)
# print(f"Accuracy is {round(acc, 4)}.")







if __name__ == "__main__":
    # Your Python logic goes here

    p2=snif()
    results = {
        "accuracy": round(acc, 4),

        # "predictions": predictions.tolist(),
        "sniffed_packets":p2
    }

    with open("results.json", "w") as outfile:
        json.dump(results, outfile)
    
    print(json.dumps(results))







