from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import os
#important that tensorflow version is 2.15.0
#run pip install tensorflow==2.15.0 if wrong version

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            print("TensorFlow Version:", tf.__version__)
            print("Current Working Directory:", os.getcwd())
            print("Contents of Current Directory:", os.listdir())
            
            model = load_model('StockV2.keras') 
            print("Model Loaded Successfully")
            
            data = []
            for i in range(1, 6):
                data.append(float(request.form.get(f'open{i}')))
                data.append(float(request.form.get(f'close{i}')))
                data.append(float(request.form.get(f'high{i}')))
                data.append(float(request.form.get(f'low{i}')))
            
            input_data = np.array([data])


            print("Input Data:", input_data)

            # Make prediction
            predictions = model.predict(input_data)

            # Format predictions as a list of lists
            predictions_list = predictions.tolist()

            # Return predictions as JSON
            return jsonify(predictions=predictions_list)
        
        except Exception as e:
            print("Error Loading Model:", e)
            return render_template('index.html', error=str(e))
    else:
        print("hello")
        return render_template('index.html', predictions=None, console_logs=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
