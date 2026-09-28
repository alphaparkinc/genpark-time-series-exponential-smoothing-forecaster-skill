import sys, json
from client import TimeSeriesExponentialSmoothingForecaster

def main():
    engine = TimeSeriesExponentialSmoothingForecaster()
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try:
            req = json.loads(line)
            method = req.get("method")
            rid = req.get("id")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "forecast", "description": "Forecast time-series.", "inputSchema": {"type": "object", "properties": {"history_values": {"type": "array"}, "horizon": {"type": "integer"}}, "required": ["history_values"]}},
                        {"name": "run_benchmark_forecaster", "description": "Run self-test.", "inputSchema": {"type": "object"}}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "forecast":
                    out = engine.forecast(args.get("history_values", []), int(args.get("horizon", 5)))
                elif tname == "run_benchmark_forecaster":
                    out = engine.run_benchmark_forecaster()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
