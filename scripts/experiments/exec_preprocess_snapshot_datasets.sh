#!/bin/bash

print_usage() {
  echo -e "\nUsage:"
  echo -e "\t-i: Input folder containing raw files"
  echo -e "\t-o: Output folder for preprocessed files"
  echo -e "\t-d: Delimiter to use (default: tab)"
  echo -e "\t-s: Number of header lines to skip (default: 4)"
}

# Parse command-line arguments
while getopts i:o:d:s: flag; do
  case "${flag}" in
    i) INPUT_FOLDER=${OPTARG};;
    o) OUTPUT_FOLDER=${OPTARG};;
    d) DELIMITER=${OPTARG};;
    s) SKIP=${OPTARG};;
    *) print_usage
       exit 1 ;;
  esac
done

# Fixed path to the binary
FILE_PREPROCESSING=/home/nikolabulat/Snapshot_Update/Tonic/build/DataPreprocessing

# Create the output folder if it doesn't exist
mkdir -p "$OUTPUT_FOLDER"

# Iterate through each file in the input folder
for INPUT_FILE in "$INPUT_FOLDER"/*; do
  FILENAME=$(basename "$INPUT_FILE")
  OUTPUT_FILE="$OUTPUT_FOLDER/preprocessed_$FILENAME"

  "$FILE_PREPROCESSING" "$INPUT_FILE" "$DELIMITER" "$SKIP" "$OUTPUT_FILE"
  echo "Processed $INPUT_FILE -> $OUTPUT_FILE"
done