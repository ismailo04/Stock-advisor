from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import model_training

app = Flask(__name__)
app.secret_key = 'tshao19'
CORS(app)


@app.route('/predict',methods=['GET'])
def predict():
    input_text = request.args.get('input')
    data = model_training.seq_model(input_text)

    # Create a response message (replace this with your actual response)
    response_message = f'Received input: {input_text}'

    # Return a JSON response
    return jsonify({'message': response_message})

@app.route('/result',methods=['GET'])
def result():
    input_text = request.args.get('input')
    file_path = f"{input_text}.txt"

    # Read the content of the text file and convert it to an array
    array_data = []
    with open(file_path, "r") as file:
        for line in file:
            # Assuming each line contains one element
            array_data.append(line.strip())
    print(array_data)
    return jsonify(array_data)

if __name__ == '__main__':
    app.run(debug=True)
