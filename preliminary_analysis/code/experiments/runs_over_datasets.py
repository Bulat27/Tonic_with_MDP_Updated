from runs_over_c import run_sweep_over_c

def run_all_datasets_sweep(dataset_configs, c_values, n_runs):
    for dataset_name, config in dataset_configs.items():
        print(f"\n\n### Running for dataset: {dataset_name} ###")
        run_sweep_over_c(
            oracle_folder=config["oracle_folder"],
            input_graph_folder=config["input_graph_folder"],
            c_values=c_values,
            base_output_folder=config["base_output_folder"],
            n_runs=n_runs
        )


if __name__ == "__main__":
    c_values = [1, 2, 3, 4, 5]
    n_runs = 50

    dataset_configs = {
        "as_733": {
            "oracle_folder": "/home/nikolabulat/sample/Tonic/oracles/as_733/nodes_practical_real",
            "input_graph_folder": "/home/nikolabulat/sample/Tonic/datasets/as_733",
            "base_output_folder": "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/outputs/as_733_uss_50_trials"
        },
        "caida": {
            "oracle_folder": "/home/nikolabulat/sample/Tonic/oracles/as_caida_122/nodes_practical_real",
            "input_graph_folder": "/home/nikolabulat/sample/Tonic/datasets/as_caida_122",
            "base_output_folder": "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/outputs/as_caida_122_uss_50_trials"
        },
        "oregon1": {
            "oracle_folder": "/home/nikolabulat/sample/Tonic/oracles/oregon/nodes_practical_real",
            "input_graph_folder": "/home/nikolabulat/sample/Tonic/datasets/oregon",
            "base_output_folder": "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/outputs/oregon1_uss_50_trials"
        }
    }

    run_all_datasets_sweep(dataset_configs, c_values, n_runs)