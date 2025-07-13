Instructions to reproduce the main experiments for Tonic with MDUpdated (Section 5.3.3). Please read the instructions in ... before contiuing.

Main results for Tonic with MDUpdated are reported in Table 2 in the paper. Here, we provide the scripts to reproduce each row in the table separately as well meta scripts to reproduce the whole table.

Before you run the scripts, you need to obtain the MinDegreepPredictor from the first snapshot. This can easily be done by following the instruction in ... to obtain the MinDegreePredictor with all degrees (percentage set to 1.0). Then, you can use the n_bar value for the first snapshot of the corresponding dataset to take only the top-n_bar nodes for the fixed MinDegreePredictor.

1 - MDUpdated, MDIncreasedSize, MDIncreasedBudget, and MDHalfHalf scripts require the following parameters: ...
For example... (I also need to emphasize the differences in parameters).

2 - MDOriginal and ExactOriginal (ExactOracle) should be run using the script "" setting the following paremeters. For example...

---

Meta scripts...

