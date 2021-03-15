# HematopoiesisAnalysis
## Data visualization, model implementation and parameter inference for mechanistic models of hematopoiesis
contains code and data accompanying

<strong>Kinetic Profiling reveals Age- and MDS-Related Changes in Hematopoietic Stem and Progenitor Cell Dynamics</strong> 

Michèle C. Buck<sup>1,\*</sup>, Lisa Bast<sup>2,3,4,\*</sup>, Alexandra Murschauser<sup>5</sup>, Judith S. Hecker<sup>1</sup>, Lea Schuh<sup>2,3</sup>,  Maja Rothenberg-Thurley<sup>6</sup>, Immanuel Andrä<sup>7</sup>, Isabel Struzina<sup>1</sup>, Moritz Thomas<sup>2</sup>, Dantong Wang<sup>2,3</sup>, Fabian J. Theis<sup>2,3</sup>, Florian Bassermann<sup>1,8</sup>, Joachim Rädler<sup>5</sup>, Klaus H. Metzeler<sup>6,8</sup>, Robert A.J. Oostendorp<sup>1</sup>, Carsten Marr<sup>2,+</sup> and Katharina S. Götze<sup>1,8,+</sup>

<sub><sup>
<sup>1</sup>Department of Medicine III, Technische Universität München, Klinikum rechts der Isar, Munich, Germany. <br>
<sup>2</sup>Institute of Computational Biology, Helmholtz Zentrum München–German Research Center for Environmental Health, Neuherberg, Germany. <br>
<sup>3</sup>Department of Mathematics, Chair of Mathematical Modeling of Biological Systems, Technische Universität München, Garching, Germany. <br>
<sup>4</sup>Laboratory of Molecular Neurobiology, Department of Medical Biochemistry and Biophysics, Karolinska Institutet, Stockholm, Sweden.<br>
<sup>5</sup>Department of soft condensed matter physics, Faculty of Physics, Ludwig-Maximilians-Universität, Munich, Germany. <br>
<sup>6</sup>Laboratory for Leukemia Diagnostics, Department of Medicine III, Ludwig-Maximilians-Universität, Munich, Germany. <br>
<sup>7</sup>Institute of Microbiology, Technische Universität München, Munich, Germany. <br>
<sup>8</sup>German Cancer Consortium (DKTK), Heidelberg, Partner Site Munich. <br>
<sup>*</sup> Equal contribution <br>
<sup>+</sup> Joint corresponding authors <br>
</sup></sub>

 required software: 
- MATLAB (R2017a), usage of Toolboxes:
  - PESTO (https://github.com/ICB-DCM/PESTO/)
  - AMICI (https://github.com/ICB-DCM/AMICI) 
  - STRIKEGOLDD (https://github.com/afvillaverde/strike-goldd_2.1)
 
  which are already included in folder 'tools' but need to get unzipped. Note that AMICI uses '.mex' files and requires MinGW as C/C++ compiler.   If you have not used mex with MATLAB before you might need to set it up first (by following these instructions: https://de.mathworks.com/help/matlab/matlab_external/install-mingw-support-package.html).
  
- Python (3.4), usage of libraries:
  - pandas
  - numpy
  - math
  - seaborn
  - matplotlib
  - scipy
  - fnmatch
  - sklearn
  - statsmodels
  - h5py
  - random
  - collections
  - os
  - re

<h2>Data visualization</h2> 
<h3>Bulk cell culture FACS analysis</h3> 
To explore data set and perform statisical tests for group comparisons 

  1. go to folder <strong>/Python/data_analysis/</strong> and run <strong>Hematopoiesis_Graphics_Data.ipynb</strong>.
  
  2. Functions for data loading and plotting can be found in <strong>defined_functions.ipynb</strong>.
  

<h2>Structural identifiability analysis for multi-compartmental model</h2>
To perform structural identifiability analysis go to <strong>./Structural_Identifiability_Analysis/</strong>.

  1. open <strong>structural_identifiability_main.m</strong> and specify the directories and settings in <strong>getSISettings()</strong>.
    
  2. run <strong>structural_identifiability_main.m</strong>.
  
    
<h2>Comparison of MDS patients, CHIP individuals and healthy individuals</h2> 

<h3>Parameter inference on bulk cell culture FACS data</h3>
    
  1. Specify settings in <strong>./MATLAB/parameter_inference/getDisorderAnalysisSettings.m</strong> to perform parameter inference on experimental (opt.RUN = 'fit_samples') or simulated (opt.RUN = 'in_silico') data.

  2. Run <strong>./MATLAB/parameter_inference/disorder_analysis_main.m</strong>. This creates a results folder according to the specified settings.
    
  3. Run <strong>build_scores_matrix_main.m</strong> for respective results folder/ settings.

 
<h3>Results visualization</h3> 
Go to <strong>./Python/results_visualization/</strong> and run 

  1. <strong>Hematopoiesis_Graphics_Results_fitSamplesRun_Model_intersect_ABDGI.ipynb</strong> to vizualize results for parameter inference on experimental data with Model_intersect_ABDGI.
 
  3. <strong>results_visualization_testRun.ipynb</strong> to visualize results for parameter inference on simulated data.
 
  5. <strong>results_visualization_validation.ipynb</strong> to visualize validation results.
 
  6. Functions for data loading and plotting can be found in <strong>definedFunctions.ipynb</strong>.
