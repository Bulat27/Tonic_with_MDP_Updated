import subprocess
import time
import yaml

def launch_independent_runs(dataset_folders, oracle_exact_paths, oracle_min_paths, names, n_trials):
    assert len(dataset_folders) == len(oracle_exact_paths) == len(oracle_min_paths) == len(names), \
        "All dataset-related lists must be the same length."

    processes = []

    for i in range(len(dataset_folders)):
        dataset_folder = dataset_folders[i]
        oracle_exact = oracle_exact_paths[i]
        oracle_min = oracle_min_paths[i]
        name = names[i]

        cmd = [
            "bash", "exec_snapshots_tonic.sh",
            "-d", dataset_folder,
            "-o", oracle_exact,
            "-i", oracle_min,
            "-t", str(n_trials),
            "-n", name
        ]

        print(f"Launching: {' '.join(cmd)}")
        p = subprocess.Popen(cmd)
        processes.append((name, p))
        time.sleep(1)  # Optional delay to avoid overloading

    print("\nAll processes launched. Waiting for completion...\n")

    for name, p in processes:
        retcode = p.wait()
        print(f"{name} finished with exit code {retcode}")


if __name__ == "__main__":
    with open("config_tonic.yaml", "r") as f:
        config = yaml.safe_load(f)

    dataset_folders = config["dataset_folders"]
    oracle_exact_paths = config["oracle_exact_paths"]
    oracle_min_paths = config["oracle_min_paths"]
    names = config["names"]
    n_trials = config["n_trials"]

    launch_independent_runs(dataset_folders, oracle_exact_paths, oracle_min_paths, names, n_trials)