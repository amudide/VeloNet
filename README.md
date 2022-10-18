# Velorama

To run on a custom dataset, create a new folder within the "data_sets" folder. Place four CSV files in your folder: U.csv, S.csv, T.csv and gt_GRN.csv. U = unspliced counts, S = spliced counts, T = total counts, gt_GRN = ground truth gene regulatory network. The U and S matrices are unnecessary if you only wish to use pseudotime.

Then, adjust the hyperparameters within run.py. Values can be set to their defaults, with the exception of the 'trial' parameter, which must be the name of the new folder within "data_sets". To incorporate RNA velocity, set "velo" to True. Then, run "run.py". Output files will be generated within the "img" folder. To evaluate your prediction, run "evaluate.py".
