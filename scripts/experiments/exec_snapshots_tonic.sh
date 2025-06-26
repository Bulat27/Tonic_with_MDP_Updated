#!/bin/bash

print_usage() {
  echo -e "\n!!! Run this script inside <scripts> folder!!! \nScript usage:\n"
	echo -e "Script usage:\n"
	echo -e "\t-d: Dataset Folder for graph sequence\n"
	echo -e "\t-o: Oracle exact path (for Tonic)\n"
	echo -e "\t-i: MinDegreePredictor path (for Tonic) \n"
	echo -e "\t-t: Number of Trials for each parametrization\n"
	echo -e "\t-n: Name (for output saving path)\n"
}

while getopts d:o:i:t:n: flag; do
	case "${flag}" in
		d) DATASET_FOLDER=${OPTARG};;
		o) ORACLE_EXACT_PATH=${OPTARG};;
		i) ORACLE_MIN_DEGREE_PATH=${OPTARG};;
		t) N_TRIALS=${OPTARG};;
    n) NAME=${OPTARG};;
		*) print_usage
		   exit 1 ;;
	esac
done

mkdir output
mkdir output/SnapshotExperiments
OUTPUT=output/SnapshotExperiments/$NAME
rm -rf $OUTPUT && mkdir $OUTPUT

RANDOM_SEED=4177
END=$(($RANDOM_SEED + $N_TRIALS - 1))

FILE_TONIC=/home/nikolabulat/Snapshot_Update/Tonic/build/Tonic
FILE_EXACT=/home/nikolabulat/Snapshot_Update/Tonic/build/RunExactAlgo

OUTPUT_PATH_TONIC=$OUTPUT/output_tonic_$NAME
OUTPUT_PATH_EXACT=$OUTPUT/output_exact_$NAME

# LIST ALL THE FILES IN THE DATASET DIR
for DATASET_PATH in "$DATASET_FOLDER"/*; do

  # -- Run Exact Algorithm to Retrieve Ground Truth
  $FILE_EXACT 0 $DATASET_PATH $OUTPUT_PATH_EXACT

  # -- Retrieve the ground truth from the Exact Algorithm output
  last_lines=$( tail -n 3 $OUTPUT_PATH_EXACT )
  echo "$last_lines"
  chunks=($last_lines)
  # -- sets up the (integer) memory budget
  TOTAL_M=${chunks[5]}

  PERC_K=0.1
  MEMORY_BUDGET=$(echo "$PERC_K * $TOTAL_M" | bc)
  MEMORY_BUDGET=${MEMORY_BUDGET%.*}
  echo "Total number of edges: $TOTAL_M"
  echo "Memory Budget: $MEMORY_BUDGET"

  # -- TONIC EXECUTION (Exact and MinDegree)
  for r in $( seq $RANDOM_SEED $END ); do
    $FILE_TONIC 0 $r $MEMORY_BUDGET 0.05 0.2 $DATASET_PATH $ORACLE_EXACT_PATH edges $OUTPUT_PATH_TONIC'_exact'
    $FILE_TONIC 0 $r $MEMORY_BUDGET 0.05 0.2 $DATASET_PATH $ORACLE_MIN_DEGREE_PATH nodes $OUTPUT_PATH_TONIC'_min_degree'
  done

done
