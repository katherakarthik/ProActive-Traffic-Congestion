import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("C:/Users/karth/Downloads/Traffic.csv")

# Feature Engineering
df['Hour'] = pd.to_datetime(df['Time']).dt.hour

day_map = {
    'Monday':1,'Tuesday':2,'Wednesday':3,
    'Thursday':4,'Friday':5,'Saturday':6,'Sunday':7
}
df['Day_of_week'] = df['Day of the week'].map(day_map)

# Add Total feature (IMPORTANT)
df['Total'] = df['CarCount'] + df['BikeCount'] + df['BusCount'] + df['TruckCount']

# Encode target
traffic_map = {'low':0,'normal':1,'heavy':2,'high':3}
df['Traffic_Label'] = df['Traffic Situation'].map(traffic_map)

# Features & target
X = df[['Hour','Day_of_week','CarCount','BikeCount','BusCount','TruckCount','Total']]
y = df['Traffic_Label']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(class_weight="balanced", random_state=42)
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained and saved as model.pkl")