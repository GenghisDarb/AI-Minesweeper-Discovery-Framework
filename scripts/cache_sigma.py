import json
import os


def cache_sigma(sigma_value):
    cache_path = "reports/evidence_state.json"
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            cached_data = json.load(f)
        if cached_data.get("sigma") == sigma_value:
            print("Sigma value unchanged. Skipping update.")
            return

    with open(cache_path, "w") as f:
        json.dump({"sigma": sigma_value}, f)
    print("Sigma value updated.")


if __name__ == "__main__":
    # Example usage
    new_sigma = 8.0  # Replace with actual computation
    cache_sigma(new_sigma)
