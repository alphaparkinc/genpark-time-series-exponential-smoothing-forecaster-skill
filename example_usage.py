from client import TimeSeriesExponentialSmoothingForecaster
import json

def main():
    forecaster = TimeSeriesExponentialSmoothingForecaster()
    res = forecaster.run_benchmark_forecaster()
    print("Forecaster Benchmark Result:")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
