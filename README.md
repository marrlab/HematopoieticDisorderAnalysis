# HematopoiesisAnalysis
## Data visualization, model implementation and parameter inference for mechanistic models of hematopoiesis
contains code and data accompanying

<strong>Kinetic Profiling reveals Age- and MDS-Related Changes in Hematopoietic Stem and Progenitor Cell Dynamics</strong> 

Michèle C. Buck<sup>1,\*</sup>, Lisa Bast<sup>2,3,4,\*</sup>, Alexandra Murschauser<sup>5</sup>, Judith S. Hecker<sup>1</sup>,Lea Schuh<sup>2,3</sup>,  Maja Rothenberg-Thurley<sup>6</sup>, Immanuel Andrä<sup>7</sup>, Isabel Struzina<sup>1</sup>, Moritz Thomas<sup>2</sup>, Dantong Wang<sup>2,3</sup>, Fabian J. Theis<sup>2,3</sup>, Florian Bassermann<sup>1,8</sup>, Joachim Rädler<sup>5</sup>, Klaus H. Metzeler<sup>6,8</sup>, Robert A.J. Oostendorp<sup>1</sup>, Carsten Marr<sup>2,+</sup> and Katharina S. Götze<sup>1,8,+</sup>

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
 
  which are already included in folder 'tools' but need to get unzipped. Note that AMICI uses '.mex' files and requires a C/C++ compiler.   If you have not used mex with MATLAB before you might need to set it up first (by using the command 'mex -setup').
  
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

  1. go to folder <strong>/DataVisualization/BulkAnalysis</strong> and run <strong>Hematopoiesis_Graphics_Data.ipynb</strong>.
  
  2. Functions for data loading and plotting can be found in <strong>defined_functions.ipynb</strong>.
  
<h3>Single-cell time-lapse analysis</h3> 

  1. go to folder <strong>/DataVisualization/SingleCellAnalysis/Plotting</strong> and run <strong>Plotting.py</strong> to plot trees.
  
  2. The data of the single-cell time-lapse experiments can be found in folder <strong>/TreeDataForPlotting</strong>.
  

<h2>Structural identifiability analysis for multi-compartmental model</h2>
To perform structural identifiability analysis go to <strong>./Structural_Identifiability_Analysis</strong>.

  1. specify the directories in <strong>setPaths()</strong>.
    
  2. run <strong>Create_Structural_Identifiability_Files.m</strong>.
  
    
<h2>Comparison of MDS patients and healthy individuals</h2> 

Download the required data and code from folder 

  1. <strong>AnalysisAndModeling/BulkAnalysis/Healthy_MDS_Comparison</strong> for bulk cell culture FACS analysis
  
  2. <strong>AnalysisAndModeling/SingleCellAnalysis</strong> for single cell time lapse analysis
  

<h3>Parameter inference on bulk cell culture FACS data</h3>
First specify the directories in <strong>setPaths()</strong>. To perform parameter inference on experimental data go to <strong>./Parameter_Inference</strong> and open <strong>RUN_H.m</strong>. Specify
    
  1. opt.RUN = 'fit_samples' to perform parameter inference on experimental data.

   1. for samples from healthy donors open <strong>getAppSettings.m</strong> and specify opt.group=‘healthy’.
        
   2. for samples from MDS patients open <strong>getAppSettings.m</strong> and specify opt.group=‘MDS’.
        
  2. opt.RUN = ‘test_inference_procedure' to perform parameter inference on simulated data.
    
  3. run <strong>RUN_H.m</strong>.
  
 
<h3>Results visualization</h3> 
Go to <strong>Hematopoiesis_Healthy_MDS_Comparison/Parameter_Inference</strong> and run <strong>Hematopoiesis_Graphics_Results_fitSamplesRun.ipynb</strong> to vizualize results for parameter inference on experimental data.
