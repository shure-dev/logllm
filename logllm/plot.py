import json
import numpy as np
import matplotlib.pyplot as plt

def plot_metrics(*models_results):
    # Process each model to ensure it's in dictionary format
    processed_models = []
    for model in models_results:
        # Convert to dictionary if the input is a JSON string
        if isinstance(model, str):
            model = json.loads(model)  # Convert string to dictionary
        processed_models.append(model)

    # Define keys to exclude from the plot
    exclude_keys = {'cache_size', 'random_state_tts', 'random_state', 'random_state_1', 'n_estimators'}

    # Initialize containers for metrics, values, and model names
    metrics = []
    model_names = []
    model_values = {}

    for model in processed_models:
        model_name = model.get("model_name", "Test Model")
        model_names.append(model_name)

        for key, value in model.items():
            if key.startswith("result_name_"):
                metric_name = value
                metric_index = key.split("_")[-1]  # Extract the index (e.g., "1" from "result_name_1")
                metric_value = model.get(f"result_value_{metric_index}", None)

                if metric_value is not None:
                    if metric_name not in metrics:
                        metrics.append(metric_name)
                    if metric_name not in model_values:
                        model_values[metric_name] = []

                    # Add the metric value to the list
                    model_values[metric_name].append(metric_value)

        # Handle additional numeric values in the model (not using the result_name format)
        for key, value in model.items():
            # Exclude specific keys and ensure the value is numeric
            if key not in exclude_keys and isinstance(value, (int, float)):
                if key not in metrics:
                    metrics.append(key)
                if key not in model_values:
                    model_values[key] = []
                model_values[key].append(value)

    # Handle cases where no valid metrics were provided
    if not metrics or not model_names:
        print("No valid metrics or model names found.")
        return

    # Ensure all models have values for all metrics, filling in with 0 if not available
    for metric in metrics:
        for i in range(len(model_names)):
            if len(model_values[metric]) <= i:
                model_values[metric].append(0)  # Default value if missing

    # Plotting side-by-side bar chart
    x = np.arange(len(metrics))  # Label locations
    bar_width = 0.15  # Width of the bars
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a bar for each model's performance metrics
    for i, model_name in enumerate(model_names):
        values = [model_values[metric][i] for metric in metrics]
        ax.bar(x + i * bar_width, values, width=bar_width, label=model_name)

    # Customization of the plot
    ax.set_xlabel('Metric', fontsize=14)
    ax.set_ylabel('Value', fontsize=14)
    ax.set_title('Comparison of Model Performance Metrics', fontsize=16)
    ax.set_xticks(x + bar_width * (len(model_names) - 1) / 2)
    ax.set_xticklabels(metrics, fontsize=12)
    ax.legend(title='Models')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()


