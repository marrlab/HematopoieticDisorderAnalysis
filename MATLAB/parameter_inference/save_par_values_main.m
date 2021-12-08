close all;
clear;
clc;

[opt] = setPaths();
fileName = '2020_08_data.xlsx';
group_str =  'healthy';%'MDS';%
bool_fit_repetitions_seperately=false;%true;%

if strcmp(group_str,'MDS')
    %individuals sorted by risk factor
    if bool_fit_repetitions_seperately==true
        %individual_IDs = {'227_1','373_1','326_1','360_1','135_1','354_1','140_1','279_1','377_1','620_1'};
        individual_IDs = {'373_1','326_1','360_1','227_1','135_1','354_1','279_1','377_1','140_1','620_1'};
    else
        %individual_IDs = {'227','373','326','360','135','354','140','279','377','620'};
        individual_IDs = {'373','326','360','227','135','354','279','377','140','620'};
    end
else
    if bool_fit_repetitions_seperately==true
        individual_IDs = {'353_1','657_1','311_1','380_1','791_1','607_1','312_1','312_2','559_1','345_1','391_1','391_2','560_1', '561_1', '348_1', '552_1', '775_1'};   
    else
        individual_IDs = {'353','657','311','380','791','607','312','559','345','391','560', '561', '348', '552', '775'};  
    end
    %individual_IDs = sort(getIndividuals(fileName,group_str,bool_fit_repetitions_seperately));
   
    %healthy: '311'    '312'    '345'    '348'    '353'    '370'    '380'    '391'    '439'    '482'    '500'    '508'    '519'    '520'    '522'    '547'    '552'    '559'    '560'    '561'    '607'    '657'    '775'    '791'
    %MDS: '135'    '140'    '227'    '279'    '326'    '354'    '360'    '373'    '377'    '620'
    % individual_IDs = {'353_1','345_1','559_1','560_1','482_1','522_1'};
    % individual_IDs = {'1'};%,'2','3'};
end

opt_RUN = 'fit_samples';%'test_inference_procedure';%%'hierarchy_comparison_BIC';%


% for n_is = 5
%     saveValues(opt_RUN,opt_group,bool_fit_repetitions_seperately,n_is,individual_IDs,sim_model_str,opt_model_str,noise_level)
% end

n_is=3;

sim_model_str = {'model_intersect_ABDGI'};%{'model_A'};
opt_model_str = {'model_intersect_ABDGI'};%{'model_A'};

% sim_model_str = {'model_A','model_B','model_C','model_D','model_E','model_F','model_G','model_H','model_I','model_J'};
% opt_model_str = {'model_A','model_B','model_C','model_D','model_E','model_F','model_G','model_H','model_I','model_J'};

noise_level = {'weak','middle','strong'};
saveValues(opt_RUN,bool_fit_repetitions_seperately,n_is,individual_IDs,group_str,sim_model_str,opt_model_str,noise_level)

function [opt] = setPaths()
    opt.c_path = cd;
    cd('../');
    path1=cd;
    addpath(genpath(fullfile(path1,'utils')));
    addpath(genpath(fullfile(path1,'toolboxes')));
    addpath(genpath(fullfile(path1,'toolboxes','AMICI-master')));
    opt.a_path = fullfile(path1,'toolboxes','AMICI-master','matlab','examples');
    opt.pythonDataVisualization_path = fullfile(opt.c_path);
    cd(opt.c_path);
end