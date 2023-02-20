import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pmdarima as pm
import statsmodels.api as sm

# Read in the data and set the index to the 'date' column
data = pd.read_csv('YearMonthDay.csv', index_col='date', parse_dates=True)
#23183.5
# Forward fill missing values
print(data)
#data = data.fillna(method='ffill')
data = data.dropna()
# Apply moving average smoothing
window_size = 7
data_smoothed = data.rolling(window_size).mean()
data_smoothed = data_smoothed.dropna()
#print(data_smoothed)
#data_smoothed = data_smoothed.interpolate()
#print(data_smoothed)
# Plot the smoothed time series data
plt.plot(data_smoothed)
plt.title("Players vs. Time")
plt.xlabel("Time")
plt.ylabel("Players")
# Remove trend component
trend = data_smoothed.diff().dropna()
data_detrended = data - trend
data_detrended = data_detrended.dropna()
print(data_detrended)

# Fit ARIMA model
model = pm.auto_arima(data_detrended, seasonal=False, error_action='ignore', suppress_warnings=True)

# Generate predictions for the next 2 months
preds, conf_int = model.predict(n_periods=60, return_conf_int=True)

# Plot the predicted values and confidence intervals
plt.plot(data_detrended.loc['2022':])
plt.plot(preds, color='red')
plt.fill_between(np.arange(len(data_detrended), len(data_detrended)+len(preds)), conf_int[:, 0], conf_int[:, 1], alpha=0.1, color='gray')
plt.xlim(pd.to_datetime('2022-1-01'), pd.to_datetime('2023-04-01'))
plt.xticks(pd.date_range(start='2022-01-01', end='2023-04-01', freq='3M'))
pred_value, conf_int = model.predict(start='2023-03-01', end='2023-03-01', return_conf_int=True, alpha=0.2)
lower_bound, upper_bound = conf_int[0]
print("Predicted value for 2023-03-01:", pred_value)
print("Lower bound of 80% confidence interval:", lower_bound)
print("Upper bound of 80% confidence interval:", upper_bound)
plt.show()
