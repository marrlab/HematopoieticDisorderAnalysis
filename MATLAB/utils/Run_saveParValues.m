close all;
clear;
clc;


individual_IDs = {'1'};%,'2','3'};
% individual_IDs = sort(getIndividuals(fileName,group_str{g_id},false,bool_fit_repetitions_seperately));
% individual_IDs = {'353_1','345_1','559_1','560_1','482_1','522_1'};

opt_RUN = 'test_inference_procedure';%'fit_samples';%'hierarchy_comparison_BIC';%

opt_group = 'healthy';%'MDS'

bool_fit_repetitions_seperately = true;

% for n_is = 5
%     saveValues(opt_RUN,opt_group,bool_fit_repetitions_seperately,n_is,individual_IDs,sim_model_str,opt_model_str,noise_level)
% end

n_is=3;

sim_model_str = {'model_A'};
opt_model_str = {'model_A'};

% sim_model_str = {'model_A','model_B','model_C','model_D','model_E','model_F','model_G','model_H','model_I','model_J'};
% opt_model_str = {'model_A','model_B','model_C','model_D','model_E','model_F','model_G','model_H','model_I','model_J'};

noise_level = {'weak','middle','strong'};
saveValues(opt_RUN,opt_group,bool_fit_repetitions_seperately,n_is,individual_IDs,sim_model_str,opt_model_str,noise_level)
