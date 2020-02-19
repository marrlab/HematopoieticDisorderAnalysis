function [opt,nl_end] = getAppSettings(opt)

opt.group = 'healthy';%'MDS';

%% model states
opt.models_implemented = {'model_A','model_B','model_C','model_D','model_E','model_F','model_G','model_H','model_I','model_J'};
opt.model = 'model_A';
opt.fitDeadCells = false;%true;
% for fitting number of divisions:
opt.n_divStates = 7;
if opt.n_divStates>1
    opt.modelAccumulateInLastState = true;
else
    opt.modelAccumulateInLastState = false;
end
opt.fit_repetitions_seperately = true;
opt.n_intermediateStates = 3;
opt.iS_ID = 1;
        
%% transformation of parameters:
% opt.parScale ='log10'; 
opt.parScale ='partly_log10'; %everything log10 transformed except initital conditions
% opt.parScale='none';

%% constraints on parameters:
opt.applyParConstraints = false;

%% noise model:
% opt.noiseType = 'LogLaplace';
opt.noiseType = 'LogNormal'; %--> most appropriate

%% optimization settings
opt.PLcalculation = false;%true; %calculation of profile likelihoods
opt.CI_levels = [0.9,0.95,0.99]; %levels for PL-confidence intervals
opt.optimizationMode = 'hierarchical';%'standard';%
opt.testGradient = true;%false;

%% for plotting the (simulated/ experimental) data
% opt.dataType = 'totalNumbers'; 
% opt.dataType = 'percentages'; 
% opt.dataType = 'logTotalNumbers';
opt.dataType = 'log2TotalNumbers';
% opt.dataType = 'log10TotalNumbers';
  
%% storing restructured data/ adapted simulation files/ results
opt.save = true;
opt.exportData4Monolix= false;%true;    
opt.exportData4Python = true;%false;
opt.exportResults4Python = true;%false;%if set to false, data will be plotted with MATLAB

%initialize values
opt.noiseLevel='';%overwritten later if required
model_str=[];
switch opt.RUN
    case 'fit_samples'
        %% data settings
        opt.realdata = true;
        opt.fileName = '2019_07_data.xlsx';
        opt.fitInitialConds = true;%false;%
        [opt.individuals,~] = getIndividuals(opt.fileName,opt.group,opt.fit_repetitions_seperately);
        opt.n_individuals = length(opt.individuals);
        opt.applyNoise = false;
    case 'test_inference_procedure'
        opt.model_sim = 'model_A';
        opt.realdata = false;
        opt.applyNoise = true;
        if opt.applyNoise == true
            opt.noiseLevel = {'weak','middle','strong','realistic',};
        end
        opt.n_replicates=1; %determine nr of samples
        opt.n_repetitions=1;%determine nr of repititions (different initial conditions, but same rates)
        opt.n_individuals=3;
        opt.individuals = cellstr(num2str([1:opt.n_individuals]'));
        opt.fitInitialConds=true;%false;
        [opt] = getSimulationSettings(opt);
end

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

%how many noise level iterations?
if opt.applyNoise
    if iscell(opt.noiseLevel)
        nl_end = length(opt.noiseLevel);
    else
        nl_end=1;
        opt = getNoiseSettings(opt,opt.noiseLevel);
    end
else
    nl_end=1;
end

opt.structuralIdentifiability=false;
opt.validation=false;
%for plotting: specify colors for cell types
opt.c_map =[204 0 0; %HSCs
            255 128 0; %MPP 
            0 51 102;  %MLP
            102 0 204; %CMP 
            0 153 76;  %GMP 
            87 215 247;  %MEP
            255 224 14; %mature cells
            160 160 160]./255;%dead cells dunkler

%AMICI options (builds symbolic model files)
opt.amiOptions = amioption('sensi',1,...
                           'maxsteps',1e9,...
                           'atol', 1e-8, ...
                           'rtol', 1e-6);
end