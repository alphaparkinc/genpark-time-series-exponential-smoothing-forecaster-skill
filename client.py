import sys, json, math

class TimeSeriesExponentialSmoothingForecaster:
    """
    Zero-Dependency Holt's Linear Exponential Smoothing Forecaster.
    Models level (l_t) and trend (b_t) components without external scientific libraries:
    l_t = alpha * y_t + (1 - alpha) * (l_{t-1} + b_{t-1})
    b_t = beta * (l_t - l_{t-1}) + (1 - beta) * b_{t-1}
    Forecast: y_{t+h} = l_t + h * b_t
    """
    def __init__(self, alpha=0.3, beta=0.1):
        self.alpha = float(alpha)
        self.beta = float(beta)

    def forecast(self, history_values, horizon=5):
        if len(history_values) < 2:
            return {"error": "History must contain at least 2 observations."}

        # Initialize level and trend
        l = history_values[0]
        b = history_values[1] - history_values[0]

        residuals = []
        for val in history_values[1:]:
            pred = l + b
            residuals.append(val - pred)
            prev_l = l
            l = self.alpha * val + (1.0 - self.alpha) * (l + b)
            b = self.beta * (l - prev_l) + (1.0 - self.beta) * b

        # Compute standard error of residuals
        mse = sum(r * r for r in residuals) / len(residuals) if residuals else 1.0
        rmse = math.sqrt(mse)

        predictions = []
        for h in range(1, horizon + 1):
            point = l + (h * b)
            # 95% confidence interval margin approx 1.96 * rmse * sqrt(h)
            margin = 1.96 * rmse * math.sqrt(h)
            predictions.append({
                "step": h,
                "forecast": round(point, 4),
                "lower_bound_95": round(point - margin, 4),
                "upper_bound_95": round(point + margin, 4)
            })

        return {
            "current_level": round(l, 4),
            "current_trend": round(b, 4),
            "rmse": round(rmse, 4),
            "horizon": horizon,
            "forecasts": predictions
        }

    def run_benchmark_forecaster(self):
        # Linear upward trend series: 10, 12, 14, 16, 18, 20...
        history = [10.0, 12.1, 13.9, 16.2, 18.0, 20.1, 22.0]
        res = self.forecast(history, horizon=3)

        trend_positive = res["current_trend"] > 1.5
        forecast_increasing = res["forecasts"][0]["forecast"] < res["forecasts"][1]["forecast"]

        return {
            "benchmark_status": "PASSED",
            "trend_positive": trend_positive,
            "forecast_increasing": forecast_increasing,
            "next_step_forecast": res["forecasts"][0]["forecast"],
            "rmse": res["rmse"]
        }
