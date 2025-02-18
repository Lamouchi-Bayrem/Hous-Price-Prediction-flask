from flask import Flask, render_template, request
import pickle
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///home_prices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Define Database Model
class HomeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Float, nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    predicted_price = db.Column(db.Float)
    
# Load the trained model
with open('home_price_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# Form Submission Route
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get form data
            area = float(request.form['area'])
            rooms = int(request.form['rooms'])
            age = int(request.form['age'])

            # Create a DataFrame with named columns to match the model's expected input
            input_data = pd.DataFrame([[area, rooms, age]], columns=['area', 'rooms', 'age'])

            # Make prediction
            predicted_price = model.predict(input_data)[0]

            # Save to Database
            new_entry = HomeData(area=area, rooms=rooms, age=age, predicted_price=predicted_price)
            db.session.add(new_entry)
            db.session.commit()

            return render_template('index.html', prediction_text=f'Predicted Home Price: ${predicted_price:,.2f}')

        except Exception as e:
            return render_template('index.html', error_text=f"Error: {str(e)}")

# Admin Route to View Database Contents
@app.route('/admin')
def admin():
    # Query all records from the database
    all_data = HomeData.query.all()
    return render_template('admin.html', data=all_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(host='0.0.0.0', debug=True, port=5001)
