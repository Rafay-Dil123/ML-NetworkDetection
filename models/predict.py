from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import numpy as np
import clf




def packet_handler(packet):
    # Extract basic features (expand as per dataset features)
    features_dict = {
    "duration": 1,  # Duration tracking requires session state; set to a default for single packets
    "src_bytes": len(packet.payload),
    "dst_bytes": len(packet),
    "count": 1,  # Default count per packet
    "srv_count": 1,  # Count of service sessions (single packet)
}

    # Convert to DataFrame
    packet_df = pd.DataFrame([features_dict])

    # Apply pre-trained scaler
    packet_df_scaled = scaler.transform(packet_df)

    # Predict
    prediction = clf.predict(packet_df_scaled)
    print(f"Packet Prediction: {prediction}")

# Capture packets (adjust count or filter as needed)
sniff(prn=packet_handler, count=10)  # Capture 10 packets for testing