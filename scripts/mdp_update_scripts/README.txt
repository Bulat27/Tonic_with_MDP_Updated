Instructions to reproduce the experiments for Tonic with MDUpdated.

The experiments are split in two parts:

1 - Preliminary analysis, which includes the results for MDSimilarity and USS experiments (Section 5.3.1 and Section 5.3.2 in the paper)
2 - Tonic with the Updated MinDegreePredictor (Section 5.3.3)

In this file, we explain the general structure of the experiments as well as the common steps required for both
the preliminary analysis and the final results. Additional steps required to reproduce the results are explained
in the corresponding subfolders.

Scripts to reproduce the preliminary analysis can be found in the ./preliminary_analysis_experiments subfolder, while the scripts for the final experiments are in ./tonic_with_uss_experiments. Both folders contain two types of scripts. The first type is used to run one of the experiments from the corresponding section separetely. The second type represents a meta script that allows the user to simply reproduce all the results for a Figure or a Table. For each meta script, a config file is provided to specify the paths. This allows a user the flexibility to save the data at arbitrary paths, while making them easy to specify in the configuration files. Please keep in mind that meta scripts currently run each individual experiment by starting and independent subprocess. In case you do not have adequate CPU resources, you might need to modify the script to run them sequentially.

Common steps required for both experiments types:

1 - Run compile.sh to compile Tonic and put the binaries in ./code/Tonic-build
2 - Download and extract snapshot datasets
3 - Follow the instructions in ... to preprocess the datasets and prepare the necessary oracle files. We provide auxiliary scripts to simplify this process. Important: Auxiliary scripts (the ones mentioned in this point) should be run from mdp_update_scripts folder (unless you want to change the relative paths).
   3.1 - Run exec_preprocess_snapshots_datasets.sh (make this .py and specify the params) to preprocess snapshot datasets
   3.2 - Run compute_nbar_snapshots.py (add the params) to obtain a .txt with n_bar values

After completing the common steps, refer to README files in the dedicated subfolder, based on the experiments you want to reproduce.