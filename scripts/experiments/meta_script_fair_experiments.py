import subprocess
import time
import yaml

def launch_independent_runs(script_name, c_values, dataset_folders, oracle_min_paths, nbar_files, base_names, n_trials):

    assert len(dataset_folders) == len(oracle_min_paths) == len(nbar_files) == len(base_names), \
        "All dataset-related lists must be the same length."

    processes = []

    for i in range(len(dataset_folders)):
        dataset_folder = dataset_folders[i]
        oracle_path = oracle_min_paths[i]
        nbar_file = nbar_files[i]
        base_name = base_names[i]

        for c in c_values:
            full_name = f"{base_name}_c{c}"

            cmd = [
                "python", script_name,
                "-d", dataset_folder,
                "-o", oracle_path,
                "-b", nbar_file,
                "-c", str(c),
                "-t", str(n_trials),
                "-n", full_name
            ]

            print(f"Launching: {' '.join(cmd)}")
            p = subprocess.Popen(cmd)
            processes.append((full_name, p))
            time.sleep(1)  # Optional: reduce simultaneous load

    print("\nAll processes launched. Waiting for completion...\n")

    for name, p in processes:
        retcode = p.wait()
        print(f"{name} finished with exit code {retcode}")


if __name__ == "__main__":
    # Load from YAML
    with open("fair_experiments.yaml", "r") as f:
        config = yaml.safe_load(f)

    script_name = config["script_name"]
    c_values = config["c_values"]
    n_trials = config["n_trials"]
    dataset_folders = config["dataset_folders"]
    oracle_min_paths = config["oracle_min_paths"]
    nbar_files = config["nbar_files"]
    base_names = config["base_names"]

    launch_independent_runs(script_name, c_values, dataset_folders, oracle_min_paths, nbar_files, base_names, n_trials)