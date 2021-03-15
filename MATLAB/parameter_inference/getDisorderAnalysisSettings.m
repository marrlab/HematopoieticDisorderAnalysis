function [opt,nl_end] = getDisorderAnalysisSettings()

opt = setPaths();

%opt.RUN = 'in_silico';
opt.RUN = 'fit_samples';

opt.group = 'healthy';%'MDS';%'CHIP';%%%

opt.structuralIdentifiability=false;

%% model simulation settings:
opt.modelStates = {'HSC','MPP','MLP','CMP','GMP','MEP','mat'};
opt.models_implemented = {'model_A','model_B','model_C','model_D','model_E','model_F','model_G','model_H','model_I','model_J','model_intersect_ABDGI'};
opt.model = 'model_intersect_ABDGI';%'model_A';

opt.fitDeadCells = false;%true;
opt.fitInitialConds=true;%false;
% for fitting number of divisions:
opt.n_divStates = 7;
if opt.n_divStates>1
    opt.modelAccumulateInLastState = true;
else
    opt.modelAccumulateInLastState = false;
end

% AMICI options:
opt.amiOptions = amioption('sensi',1,...
                           'maxsteps',1e9,...
                           'atol', 1e-8, ...
                           'rtol', 1e-6);

%% parameter inference settings:
opt.fit_repetitions_seperately = false;%true; 

%transformation of parameters during optimization:
% opt.parScale ='log10'; 
opt.parScale ='partly_log10'; %everything log10 transformed except initital conditions
% opt.parScale='none';

%constraints on parameters:
opt.applyParConstraints = false;

%noise model of logLikelihood:
% opt.noiseType = 'LogLaplace'; %--> issues with convergence
opt.noiseType = 'LogNormal'; %--> most appropriate

%profile likelihood and confidence intervals
opt.PLcalculation = true; %false; %calculation of profile likelihoods
opt.CI_levels = [0.9,0.95,0.99]; %levels for PL-confidence intervals

opt.optimizationMode = 'hierarchical';%'standard';%
opt.testGradient = false;%true;%


%% data used for fit:
switch opt.RUN 
    case 'fit_samples'
        opt.realdata = true;
        opt.fileName = '2020_08_data.xlsx';
        [opt.individuals,~] = getIndividuals(opt.fileName,opt.group,opt.fit_repetitions_seperately);
%         if strcmp(opt.group,'healthy')
%             if opt.fit_repetitions_seperately
%                 opt.individuals = {'607_1','657_1','425_1','520_1','729_1','754_1','775_1', '791_1'};
%             else
%                 opt.individuals = {'607','657','791','775','425','520','729','754'};
%             end
%         elseif strcmp(opt.group,'MDS')
%             if opt.fit_repetitions_seperately
%                 opt.individuals = {'592_1','620_1','545_1'};
%             else
%                 opt.individuals = {'592','620','545'};
%             end
%         end
        opt.n_individuals = length(opt.individuals);
        opt.applyNoise = false;
        opt.noiseLevel='';
        nl_end=1;
    case 'in_silico'
        opt.realdata = false;
        opt.fileName = '2019_07_data.xlsx'; %for test parameter results from individuals in group opt.group are loaded
        opt.model_sim = 'model_A'; %only initialization, updated later
        opt.t = [1,2,3,5,7]*24;%times at which in silico data should be observed in hours
        opt.applyNoise = true;
        if opt.applyNoise == true
            opt.noiseLevel = {'weak','middle','strong'};%,'realistic',};
        end
        nl_end=length(opt.noiseLevel);
        opt.n_individuals=5;
        opt.n_replicates=1; %determine nr of samples
        opt.n_repetitions=1;%determine nr of repititions (different initial conditions, but same rates)
        opt.individuals = cellstr(num2str([1:opt.n_individuals]'));
end

opt.n_intermediateStates = 3; 
opt.iS_ID = length(opt.n_intermediateStates); %index for intermediate state

if opt.fitInitialConds
    if opt.fit_repetitions_seperately
        opt.n_initialConds_N=1;
    elseif opt.realdata == false
        opt.n_initialConds_N = opt.n_repetitions;
    else
        opt.n_initialConds_N=1; %updated later
    end
else
    opt.n_initialConds_N=0;
end

opt.validation=false;

%% storing restructured data/ adapted simulation files/ results
opt.save = true;   
opt.parTransformationStr = {'lin','log10','ratio'}; %transformation of parameters in results array
opt.modelFitResultsTransformation = 'log2TotalNumbers'; %only important for model fit plot; 
% opt.modelFitResultsTransformation = 'totalNumbers';
% opt.modelFitResultsTransformation = 'logTotalNumbers';
% opt.modelFitResultsTransformation = 'log2TotalNumbers';
% opt.modelFitResultsTransformation = 'log10TotalNumbers';
% opt.modelFitResultsTransformation = 'percentages';

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

end


% %% storing restructured data/ adapted simulation files/ results
% opt.exportData4Monolix= false;%true;    
% opt.exportData4Python = true;%false;
% opt.exportResults4Python = true;%false;%if set to false, data will be plotted with MATLAB

% %how many noise level iterations?
% if opt.applyNoise
%     if iscell(opt.noiseLevel)
%         nl_end = length(opt.noiseLevel);
%     else
%         nl_end=1;
%         opt = getNoiseSettings(opt,opt.noiseLevel);
%     end
% else
%     nl_end=1;
% end

