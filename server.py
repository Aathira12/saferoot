from flask import Flask, jsonify
import pandas as pd
import numpy as np
import datetime as dt

app = Flask(__name__)

@app.route('/check_route', methods=['GET'])
def check_route():
    np.random.seed(42)
    vehicle_ids = [f'vehicle_{i}' for i in range(1, 11)]
    start_times = pd.date_range(start='2024-07-19 08:00:00', periods=10, freq='10T')
    end_times = start_times + pd.to_timedelta(np.random.randint(5, 15, size=10), unit='m')
    speeds = np.concatenate((np.random.uniform(50, 60, size=3), np.random.uniform(20, 30, size=7)))

    data = {
        'vehicle_id': vehicle_ids,
        'start_time': start_times,
        'end_time': end_times,
        'start_lat': np.random.uniform(34.0500, 34.0510, size=10),
        'start_lon': np.random.uniform(-118.2450, -118.2440, size=10),
        'end_lat': np.random.uniform(34.0530, 34.0540, size=10),
        'end_lon': np.random.uniform(-118.2420, -118.2410, size=10),
        'speed_kmh': speeds
    }

    df = pd.DataFrame(data)
    df['time_taken'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60
    df['distance_km'] = df['speed_kmh'] * (df['time_taken'] / 60)

    slower_vehicles_df = df[df['speed_kmh'] < 30]
    num_vehicles = len(df)
    num_rerouted = max(1, num_vehicles // 2 + 1)
    rerouted_vehicles = slower_vehicles_df.sample(n=num_rerouted)
    rerouted_vehicles['start_lat'] += np.random.uniform(-0.001, 0.001, size=len(rerouted_vehicles))
    rerouted_vehicles['start_lon'] += np.random.uniform(-0.001, 0.001, size=len(rerouted_vehicles))
    rerouted_vehicles['end_lat'] += np.random.uniform(-0.001, 0.001, size=len(rerouted_vehicles))
    rerouted_vehicles['end_lon'] += np.random.uniform(-0.001, 0.001, size=len(rerouted_vehicles))
    df.update(rerouted_vehicles)

    slow_vehicles_count = df[df['speed_kmh'] < 30].shape[0]
    fast_vehicles_count = df[df['speed_kmh'] >= 30].shape[0]
    rerouted_vehicles_count = rerouted_vehicles.shape[0]

    if rerouted_vehicles_count < (num_vehicles // 2) and fast_vehicles_count > 0:
        suitability = "suitable for travel"
    else:
        suitability = "not suitable for travel"

    result = {
        'suitability': suitability,
        'slow_vehicles_count': slow_vehicles_count,
        'fast_vehicles_count': fast_vehicles_count,
        'rerouted_vehicles_count': rerouted_vehicles_count
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
