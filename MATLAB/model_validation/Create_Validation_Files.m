%% compare model to unseen data
%author: Lisa Bast
%date: 04.11.2019

%individual MDS 279 was measured after 8 and 9 days but only observations
%for t in [0,7] were used to fit data and estimate theta

%% 1) load inference result:
opt_p = setPaths();
current_path = cd();
cd('../');
cd('./Parameter_Inference/results_fit_samples_7divs_3iS_HO_LogNormal_fit_iC/model_A_model/individual_279');
load('WS_MDS_individual_279.mat')
cd(current_path);

%% 2) some settings
opt.validation = true;
% opt.individuals = {'279'};
opt.c_path = opt_p.c_path;
opt.a_path = opt_p.a_path;
opt.pythonDataVisualization_path = opt_p.pythonDataVisualization_path;

%% 3) get data
[opt.individuals,~] = getIndividuals(opt.fileName,opt.group,opt.fit_repetitions_seperately,opt.validation);
dataPreprocessing(possibleCompartments, opt.fitInitialConds);
[data] = getObsData(opt.group,opt.modelStates,opt.individuals,1,opt,possibleCompartments);

%% 4) simulate model for optimal theta and t in [0,9] and compare model to unseen data points at day 8 and 9:
%if opt.exportResults4Python==true: store for every individual:
createSimulationFiles(opt,true,opt.model);
%a) ws_modelFitPlot.mat
opt.plotCompartmentSum = false;
plotResults([],parameters.MS.par(:,1),data,opt,n_states,opt.individuals{1},sigma_HO);

%b) ws_modelFitPlot_sum.mat
opt.plotCompartmentSum = true;
plotResults([],parameters.MS.par(:,1),data,opt,n_states,opt.individuals{1},sigma_HO);

