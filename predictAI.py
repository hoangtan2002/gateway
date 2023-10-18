import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
import time
from MQTT import *
import threading

def predict():
    # Load the data
    temperature = pd.read_json(
        "https://io.adafruit.com/api/v2/duytan2002/feeds/sensor01/data"
    ).value
    humidity = pd.read_json(
        "https://io.adafruit.com/api/v2/duytan2002/feeds/sensor02/data"
    ).value
    
    print(temperature)
    print(humidity)

    # Combine the data into a single dataframe
    data = pd.concat([temperature, humidity], axis=1)
    data.columns = ["temperature", "humidity"]

    # Split the data into training and testing sets
    train_size = int(len(data) * 0.8)
    train_data = data.iloc[:train_size, :]
    test_data = data.iloc[train_size:, :]

    # Normalize the data
    mean = train_data.mean()
    std = train_data.std()
    train_data = (train_data - mean) / std
    test_data = (test_data - mean) / std

    # Prepare the data for LSTM
    def prepare_data(data, look_back=1):
        X, y = [], []
        for i in range(len(data) - look_back - 1):
            X.append(data[i : (i + look_back), :])
            y.append(data[i + look_back, :])
        return np.array(X), np.array(y)

    look_back = 10
    train_X, train_y = prepare_data(train_data.values, look_back)
    test_X, test_y = prepare_data(test_data.values, look_back)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, input_shape=(look_back, 2)))
    model.add(Dense(2))
    model.compile(loss="mean_squared_error", optimizer="adam")

    # Train the model
    model.fit(train_X, train_y, epochs=100, batch_size=32, verbose=2)

    # Make predictions on the test data
    test_predict = model.predict(test_X)

    # Inverse transform the predictions and actual values
    test_predict = (test_predict * std.values) + mean.values
    test_y = (test_y * std.values) + mean.values

    # Select the best predicted value for temperature and humidity
    best_predict = test_predict[-1, :]
    best_predict_temperature = str(round(best_predict[0],2))
    best_predict_humidity = str(round(best_predict[1],2))
    
    return (best_predict_temperature , best_predict_humidity)

def predictionMainloop(event):
    while threading.main_thread().is_alive():
        predictedTemp, predictedHumid = predict()
        print("The prediction is: "+str(predictedHumid) + str(predictedTemp))
        client.publish("duytan2002/feeds/predictedtemp",predictedTemp)
        client.publish("duytan2002/feeds/predictedhumid",predictedHumid)
        time.sleep(10)
        pass
