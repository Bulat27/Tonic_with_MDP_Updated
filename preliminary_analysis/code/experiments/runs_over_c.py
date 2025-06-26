import os
from rerunning_experiments import run_multiple_uss_runs


def run_sweep_over_c(
    oracle_folder,
    input_graph_folder,
    c_values,
    base_output_folder,
    n_runs,
):
    for c in c_values:
        print(f"\n=== Running experiments for c = {c} ===")
        output_folder = os.path.join(base_output_folder, f"c{c}")
        run_multiple_uss_runs(
            oracle_folder=oracle_folder,
            input_graph_folder=input_graph_folder,
            c=c,
            output_folder=output_folder,
            n_runs=n_runs
        )


# if __name__ == "__main__":
#     oracle_folder = "/home/nikolabulat/sample/Tonic/oracles/as_733/nodes_practical_real"
#     input_graph_folder = "/home/nikolabulat/sample/Tonic/datasets/as_733"
#     c_values = [1, 2, 3]
#     base_output_folder = "/home/nikolabulat/Snapshot_Update/Tonic/preliminary_analysis/outputs/as_733_uss_50_trials_cpp"
#     n_runs = 50

#     run_sweep_over_c(
#         oracle_folder,
#         input_graph_folder,
#         c_values,
#         base_output_folder,
#         n_runs
#     )