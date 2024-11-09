import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

# Sample data: area (sq ft), rooms, age of house, price ($)
data = {
    'area': [1500, 2500, 1800, 2200, 1700],
    'rooms': [3, 4, 3, 5, 3],
    'age': [20, 15, 30, 10, 25],
    'price': [300000, 500000, 350000, 450000, 320000]
}

# Convert to a DataFrame
df = pd.DataFrame(data)
X = df[['area', 'rooms', 'age']]  # Features
y = df['price']  # Target variable

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the model
with open('home_price_model.pkl', 'wb') as f:
    pickle.dump(model, f)
