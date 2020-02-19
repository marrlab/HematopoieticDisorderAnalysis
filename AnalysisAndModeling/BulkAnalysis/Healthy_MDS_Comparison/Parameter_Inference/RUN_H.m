function [] = RUN_H

%% info:
% author: Lisa Bast
% date: 13.01.16
%% description:
% main function for performing MLE for ODE compartment models describing hematopoiesis or MDS,
% based on experimentally measured cell abundances
%  -    compartments describe cells belonging to a certain cell type which underwent the same number 
%       of divisions dividisions
%  -    parameters describe reaction rates 
%  -    reactions describe proliferation, differentiation and cell death
clear;
clc;
close all;

opt = setPaths();

%% general settings: what should be done?
% opt.RUN = 'test_inference_procedure';
opt.RUN = 'fit_samples';
%% specify/ change settings in getAppSettings()

switch opt.RUN
    case 'test_inference_procedure'
        str = '_test.mat';
    otherwise
        str='';
end

possibleCompartments = {'HSC','MPP','MLP','CMP','GMP','MEP','mature','dead'};
%specify first individual
firstIndividual=1;
transformation_str = {'lin','log10','ratio'};
[opt,nl_end] = getAppSettings(opt);

%% data pre-processing if necessary
if opt.realdata == true
   dataPreprocessing(possibleCompartments, opt.fitInitialConds);
end

for nl_id = 1:nl_end
    if iscell(opt.noiseLevel)
        [opt] = getNoiseSettings(opt,opt.noiseLevel{nl_id});
        opt.nL = opt.noiseLevel{nl_id};
    else
        opt.nL = opt.noiseLevel;
    end

    %% update options and simulate data if necessary
    if strcmp(opt.RUN,'test_inference_procedure') 
       opt.model_sim = opt.model;
    end
    [opt] = getResultsFolderStrings(opt);
    if opt.realdata==true
        theta_test=[];
        [~,n_states,opt] = getModelParams(opt,opt.model); %sigma is not used
        rate_names_test = [];
    else
        %create simulation file for current model & generate in
        %silico data
        if (opt.applyNoise && iscell(opt.noiseLevel))
            %update sigma
            if (strcmp(opt.noiseLevel{nl_id},'realistic') && strcmp(opt.noiseType,'LogNormal'))
                opt.sigma=getRealisticNoiseLevelFromRealDataFitResults(opt);
            end
        end
        [theta_test,n_states,opt] = getModelParams(opt,opt.model_sim);
        rate_names_test = strtrim(opt.rates(~strwcmp(opt.rates,'x0_*')));
        createSimulationFiles(opt,true,opt.model_sim)
        for i_sim_ID = 1:opt.n_individuals
            [data] = getSimData(n_states,opt,theta_test);
            save(['insilico_data_',opt.model_sim,'_',opt.noiseType,'_',opt.nL,'_individual_',opt.individuals{i_sim_ID},str],'data');
        end
        %update opt and simulation files for current model used for
        %fit
        [~,n_states,opt] = getModelParams(opt,opt.model);
    end
    %initialize values
    for i_ID=firstIndividual:opt.n_individuals
        clearvars -except firstIndividual i_ID opt model_str p_test theta_test n_states par_min par_max...
                          CI_lower CI_upper PAR_OPT_T PAR_TEST_T rate_names_test rate_names_opt transformation_str ... 
                          possibleCompartments individuals_str str rate_names_test group_str nl_id nl_end  bool_simulate...
        tic;
        if (opt.applyNoise && iscell(opt.noiseLevel))
            opt.subsubfoldername = ['individual_',opt.individuals{i_ID},'_',opt.nL,'_noise'];
        else
            opt.subsubfoldername = ['individual_',opt.individuals{i_ID}];
        end
        createResultDirs(opt.c_path,opt.foldername,opt.subfoldername,opt.subsubfoldername);
        %% get in-silico or experimental data
        [data,opt] = getData(opt,i_ID,possibleCompartments,str);
        if any(any(isnan(data.NumCellDiv_ALL{1,1})))
           continue; 
        end
        %% generate model file for optimization
        if (opt.realdata==true) || ~(strcmp(opt.model,opt.model_sim))
            bool_simulate = true;
        else
            bool_simulate = false;
        end
        createSimulationFiles(opt,bool_simulate,opt.model);

        %% optimize cost function
        [options_par, parameters, opt] = getOptimizationSettings(opt,theta_test,data);
        logL = @(theta) logL_H(theta,data,opt,i_ID);

        % define logL for storing values of sigma for optimal parameter:
        if strcmp(opt.optimizationMode,'hierarchical')
            opt.HO.save = true;
            logL_final = @(theta) logL_H(theta,data,opt,i_ID);
            opt.HO.save = false;
        end

        % test gradient
        if opt.testGradient == true
            test_and_plot_Gradient(parameters,logL,opt,i_ID)
        end

        [parameters] = optimizationProc(options_par,parameters,logL,logL_final,opt,i_ID);
        time_in_s = toc;

        % get, transform and save parameters, bounds, Confidence intervals
        individuals_str = opt.individuals;
        if i_ID==firstIndividual
            group_str = cell(opt.n_individuals,1);
            [par_min,par_max,CI_lower,CI_upper,PAR_OPT_T,PAR_TEST_T] = initializeParResult(transformation_str,opt,theta_test);
        end
        [par_min,par_max,CI_lower,CI_upper,PAR_OPT_T,PAR_TEST_T] = saveTransformedParResult(parameters,par_min,par_max,CI_lower,CI_upper,individuals_str,PAR_OPT_T,PAR_TEST_T,transformation_str,opt,theta_test,i_ID,rate_names_test);

        %% observe convergence of optimization
        MS_num(i_ID) = calculateSizeLogLPlateau(parameters);

        %% get analytically estimated sigma (in case of hierarchical optimization) 
        [sigma_HO] = getAnalyticallyEstimatedSigma(opt);

        %% 4) save results
        if opt.save
            cd(opt.c_path);
            cd(['./',opt.foldername,'/',opt.subfoldername,'/',opt.subsubfoldername]);
            save(['WS_',opt.group,'_individual_',opt.individuals{i_ID},'.mat']);
            cd(opt.c_path);
            if strcmp(opt.RUN, 'topology_comparison')
                cd(['./',opt.foldername,'/',opt.subfoldername]);
                save(['WS_',opt.group,'_Scores','.mat'],'result_Scores');
                cd(opt.c_path);
            end
        end

        %% 5) plot data/ export data for plotting graphics in Python 
        %if opt.exportResults4Python==true: store for every individual:
        %a) ws_modelFitPlot.mat
        %b) ws_modelFitPlot_sum.mat
        if opt.n_divStates>1
            opt.plotCompartmentSum = false;
            if ~opt.realdata && strcmp(opt.model_sim,opt.model)
                plotResults(theta_test,parameters.MS.par(:,1),data,opt,n_states,opt.individuals{i_ID},sigma_HO);
            else
                plotResults([],parameters.MS.par(:,1),data,opt,n_states,opt.individuals{i_ID},sigma_HO);
            end
        end
        opt.plotCompartmentSum = true;
        if ~opt.realdata && strcmp(opt.model_sim,opt.model)
            plotResults(theta_test,parameters.MS.par(:,1),data,opt,n_states,opt.individuals{i_ID},sigma_HO);
        else
            plotResults([],parameters.MS.par(:,1),data,opt,n_states,opt.individuals{i_ID},sigma_HO);
        end
    end
end
end
