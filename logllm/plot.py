import json
import matplotlib.pyplot as plt

def plot_ml_metrics(response_data):
    # Parse the JSON string into a Python dictionary if needed
    if isinstance(response_data, str):
        response_data = json.loads(response_data)

    try:
        # Define keys to exclude from the plot
        exclude_keys = {'cache_size', 'random_state_tts', 'random_state',}

        # Extract all keys and numeric values from the response, excluding specific keys
        metrics = []
        values = []
        for key, value in response_data.items():
            # Check if the key is not in the exclude list and if the value is numeric
            if key not in exclude_keys and isinstance(value, (int, float)):
                metrics.append(key)
                values.append(value)

        # Check if any numeric values were found
        if not values:
            print("No numeric values found to plot.")
            return

        # Plotting
        plt.figure(figsize=(10, 6))  # Adjusted figure size for better visualization
        plt.bar(metrics, values, color='pink')
        plt.title('Model Performance Metrics', fontsize=16)
        plt.xlabel('Parameter', fontsize=14)
        plt.ylabel('Value', fontsize=14)
        plt.ylim(0, max(values) * 1.1)  # Dynamically set the y-limit based on the maximum value
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error processing the response data: {e}")
