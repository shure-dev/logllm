import json
import matplotlib.pyplot as plt

def plot_ml_metrics(response_data):
    # Parse the JSON string into a Python dictionary if needed
    if isinstance(response_data, str):
        response_data = json.loads(response_data)

    try:
        # Extract all keys that start with "result_name_" and their corresponding "result_value_"
        metrics = []
        values = []
        for key, value in response_data.items():
            if key.startswith("result_name_"):
                metric_name = value
                metric_index = key.split("_")[-1]  # Extract the index (e.g., "1" from "result_name_1")
                metric_value = response_data.get(f"result_value_{metric_index}", None)
                
                if metric_value is not None:
                    metrics.append(metric_name)
                    values.append(metric_value)

        # Plotting
        plt.figure(figsize=(10, 6))  # Adjusted figure size for better visualization
        plt.bar(metrics, values, color='skyblue')
        plt.title('Model Performance Metrics', fontsize=16)
        plt.xlabel('Metric', fontsize=14)
        plt.ylabel('Value', fontsize=14)
        plt.ylim(0, max(values) * 1.1)  # Dynamically set the y-limit based on the maximum value
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    except TypeError as e:
        print(f"Error processing the response data: {e}")
