import subprocess
import time
import yaml

def launch_independent_runs(script_path, dataset_folders, oracle_folders, names, c_values, n_trials):
    assert len(dataset_folders) == len(oracle_folders) == len(names), \
        "Mismatch in number of datasets, oracles, and names."

    processes = []

    for i in range(len(dataset_folders)):
        for c in c_values:
            name = f"{names[i]}_c{c}"
            cmd = [
                "python", script_path,
                "-d", dataset_folders[i],
                "-o", oracle_folders[i],
                "-c", str(c),
                "-t", str(n_trials),
                "-n", name
            ]

            print(f"Launching: {' '.join(cmd)}")
            p = subprocess.Popen(cmd)
            processes.append((name, p))
            time.sleep(1)  # Optional delay

    print("\nAll processes launched. Waiting for completion...\n")

    for name, p in processes:
        retcode = p.wait()
        print(f"{name} finished with exit code {retcode}")

if __name__ == "__main__":
    with open("config_uss.yaml", "r") as f:
        config = yaml.safe_load(f)

    dataset_folders = config["dataset_folders"]
    oracle_folders = config["oracle_folders"]
    names = config["names"]
    c_values = config["c_values"]
    n_trials = config["n_trials"]

    script_path = "exec_uss_snapshot_experiments.py"
    launch_independent_runs(script_path, dataset_folders, oracle_folders, names, c_values, n_trials)