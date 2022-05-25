# HematopoiesisAnalysis
## Data visualization, model implementation and parameter inference for mechanistic models of hematopoiesis
contains code and data accompanying

<strong>Progressive Disruption of Hematopoietic Architecture from Clonal Hematopoiesis to MDS</strong> 

Michèle C. Buck<sup>1,\*</sup>, Lisa Bast<sup>2,3,4,\*</sup>, Judith S. Hecker<sup>1</sup>, Jennifer Rivière<sup>1</sup>, Maja Rothenberg-Thurley<sup>5</sup>, Luisa Vogel<sup>1</sup>, Dantong Wang<sup>2,3</sup>, Immanuel Andrä<sup>6</sup>, Fabian J. Theis<sup>2,3</sup>, Florian Bassermann<sup>1,7</sup>, Klaus H. Metzeler<sup>5,7,8</sup>, Robert A.J. Oostendorp<sup>1</sup>, Carsten Marr<sup>2,9,+</sup>, and Katharina S. Götze<sup>1,7,+</sup>

<sub><sup>
<sup>1</sup>Department of Medicine III, Technische Universität München, Klinikum rechts der Isar, Munich, Germany.
<sup>2</sup>Institute of Computational Biology, Helmholtz Zentrum München–German Research Center for Environmental Health, Neuherberg, Germany.
<sup>3</sup>Department of Mathematics, Chair of Mathematical Modeling of Biological Systems, Technische Universität München, Garching, Germany.
<sup>4</sup>Current address: Laboratory of Molecular Neurobiology, Department of Medical Biochemistry and Biophysics, Karolinska Institutet, Stockholm, Sweden.
<sup>5</sup>Laboratory for Leukemia Diagnostics, Department of Medicine III, University Hospital, Ludwig-Maximilians-Universität, Munich, Germany
<sup>6</sup>Institute of Microbiology, Technische Universität München, Munich, Germany.
<sup>7</sup>German Cancer Consortium (DKTK), Heidelberg, Partner Site Munich
<sup>8</sup>Department of Hematology and Cell Therapy, University Hospital Leipzig (UHL), Germany.
<sup>9</sup>Institute of AI for Health, Helmholtz Zentrum München–German Research Center for Environmental Health, Neuherberg, Germany.
<sup>*</sup> Equal contribution <br>
<sup>+</sup> Joint corresponding authors <br>
</sup></sub>

 required software: 
- MATLAB (R2017a), usage of Toolboxes:
  - PESTO (https://github.com/ICB-DCM/PESTO/)
  - AMICI (https://github.com/ICB-DCM/AMICI) 
  - STRIKEGOLDD (https://github.com/afvillaverde/strike-goldd_2.1)
 
  which are already included in folder 'tools' but need to get unzipped. Note that AMICI uses '.mex' files and requires MinGW as C/C++ compiler.   If you have not used mex with MATLAB before you might need to set it up first (by following these instructions: https://de.mathworks.com/help/matlab/matlab_external/install-mingw-support-package.html).
  
- Python (3.6.12) by using JupyterLab (2.2.6) and libraries:
  - pandas (1.1.5)
  - numpy (1.19.2)
  - seaborn (0.11.0)
  - matplotlib (3.3.2)
  - scipy (1.5.2)
  - scikit-learn (0.23.2)
  - statsmodels (0.12.1)
  - h5py (2.10.0)

<h2>Data visualization (Python)</h2> 
To explore data set and perform statisical tests for group comparisons 

  1. go to folder <strong>/Python/data_analysis/</strong> and run <strong>Hematopoiesis_Graphics_Data.ipynb</strong>.
  
  2. Functions for data loading and plotting can be found in <strong>defined_functions.ipynb</strong>.  

<h2>Structural identifiability analysis for multi-compartmental model (MATLAB)</h2>
To perform structural identifiability analysis go to <strong>/MATLAB/Structural_Identifiability_Analysis/</strong> run <strong>structural_identifiability_main.m</strong>. Directories and settings can be specified in <strong>getSISettings()</strong> function within the same file.
        
<h2>Comparison of MDS patients, CHIP individuals and healthy individuals</h2> 

<h3>Parameter inference on bulk cell culture FACS data (MATLAB)</h3>
    
  1. Specify settings in <strong>./MATLAB/parameter_inference/getDisorderAnalysisSettings.m</strong> to perform parameter inference on experimental (opt.RUN = 'fit_samples') or simulated (opt.RUN = 'in_silico') data.

  2. Run <strong>./MATLAB/parameter_inference/disorder_analysis_main.m</strong>. This creates a results folder according to the specified settings.
    
  3. For model selection scores tables run <strong>build_scores_matrix_main.m</strong> for respective results folder/ settings.

 
<h3>Results visualization (Python)</h3> 

To vizualize results for parameter inference on experimental data with Model_union_ABDGI go to <strong>./Python/results_visualization/</strong> and run <strong>Hematopoiesis_Graphics_Results_fitSamplesRun_Model_union_ABDGI.ipynb</strong> 
