import subprocess
import yaml

def run_md_similarity_experiments(script_name, oracle_folders, base_names):
    assert len(oracle_folders) == len(base_names), "Mismatch in oracle folders and base names"

    for oracle_folder, base_name in zip(oracle_folders, base_names):
        cmd = [
            "python", script_name,
            "-o", oracle_folder,
            "-n", base_name
        ]

        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

if __name__ == "__main__":
    with open("config_md_similarity.yaml", "r") as f:
        config = yaml.safe_load(f)

    script_name = config["script_name"]
    oracle_folders = config["oracle_folders"]
    base_names = config["base_names"]

    run_md_similarity_experiments(script_name, oracle_folders, base_names)