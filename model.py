import numpy as np
import datetime as dt
import yfinance as yf
import datetime
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM


def seq_model(stock_name):
  company = stock_name

  data = yf.download(company, start=dt.datetime(2020, 1, 1), end=dt.datetime.now())

  scaler = MinMaxScaler(feature_range=(0, 1))
  scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

  prediction_days = 120

  x_train = []
  y_train = []

  for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x - prediction_days:x, 0])
    y_train.append(scaled_data[x, 0])

  x_train, y_train = np.array(x_train), np.array(y_train)
  x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

  model = Sequential()

  model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
  model.add(Dropout(0.3))
  model.add(LSTM(units=50, return_sequences=True))
  model.add(Dropout(0.3))
  model.add(LSTM(units=50))
  model.add(Dropout(0.3))
  model.add(Dense(units=1)) #Prediction of the next closing value

  model.compile(optimizer='adam', loss='mean_squared_error')
  model.fit(x_train,y_train,epochs=25,batch_size=32)

  test_start = dt.datetime.now()
  model_inputs = scaled_data[-prediction_days:].reshape(-1, 1)
  predicted_prices_future = []
  future_days = 120
  # Loop to predict future prices
  for _ in range(future_days):
    # Reshape the input data for the model
    x_future = model_inputs[-prediction_days:].reshape(1, prediction_days, 1)

    # Use the model to predict the next day's price
    predicted_price = model.predict(x_future)[0][0]

    predicted_price += np.random.normal(0, 0.02)

    # Append the predicted price to the list
    predicted_prices_future.append(predicted_price)

    # Update the input data for the next prediction
    model_inputs = np.append(model_inputs, predicted_price)

  # Inverse transform the predicted prices to the original scale
  predicted_prices_future = scaler.inverse_transform(np.array(predicted_prices_future).reshape(-1, 1))

  file_path = f"{stock_name}.txt"

  # Write the array data to the text file
  with open(file_path, "w") as file:
    for item in predicted_prices_future:
      file.write(str(item[0]) + "\n")
  return predicted_prices_future
