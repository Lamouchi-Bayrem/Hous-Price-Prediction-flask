from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model
with open('home_price_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    area = float(request.form['area'])
    rooms = int(request.form['rooms'])
    age = int(request.form['age'])

    # Create a DataFrame with named columns to match the model's expected input
    input_data = pd.DataFrame([[area, rooms, age]], columns=['area', 'rooms', 'age'])

    # Make prediction
    prediction = model.predict(input_data)[0]

    return render_template('index.html', prediction_text=f'Predicted Home Price: ${prediction:,.2f}')

if __name__ == '__main__':
    app.run( host= '0.0.0.0' , debug=True , port=5001)
