import subprocess

def process_graph_stream(input_file, output_file_prefix, k, n_bar, seed=None):
    """
    Call the compiled RunUSS C++ binary.

    Args:
        input_file: path to edge stream
        output_file_prefix: prefix (no extension) for output file
        k: nodes to track
        n_bar: how many top nodes to output
        seed: RNG seed for reproducibility
    """
    seed = seed if seed is not None else 42
    uss_binary = "/home/nikolabulat/Snapshot_Update/Tonic/build/RunUSS"  # It should be a relative path!

    subprocess.run(
        [uss_binary, input_file, output_file_prefix, str(k), str(seed), str(n_bar)],
        check=True
    )