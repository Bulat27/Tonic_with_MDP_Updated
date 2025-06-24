import subprocess

def get_total_edges(exact_output_path):
    """ Reads the output of RunExactAlgo and extracts the total number of edges. """
    with open(exact_output_path, "r") as f:
        lines = f.readlines()
    last_line = lines[-2].strip().split()
    return int(last_line[-1])

def run_exact_algorithm(file_exact, dataset_path, output_exact):
    """ Runs the exact algorithm to get the ground truth edge count. """
    subprocess.run([file_exact, "0", dataset_path, output_exact], check=True)
    return get_total_edges(output_exact)

def read_top_k_lines(file_path, n):
    with open(file_path, 'r') as f:
        return [next(f) for _ in range(n)]