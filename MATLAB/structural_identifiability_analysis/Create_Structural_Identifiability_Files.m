opt = setPaths();

model_str={'model_A'};

%% 1. specify settings
[opt] = getAppSettings(opt);

[~,~,opt] = getModelParams(opt,model_str); 
opt.n_initialConds = 1;
adaptModelFile_SI(model_str,opt)

cd(opt.structIdent_path)

z_create_hematopoiesis_model_A

cd('../')

%% 2. Open file options.m
% make sure 'modelname = 'hematopoiesis_model_A';' is the specified option.

%% 3. Open and run file STRIKE_GOLDD.m
STRIKE_GOLDD
%results will be printed to console and stored in results folder



