function [] = disorder_analysis_main()

%% info:
% author: Lisa Bast
% date: 25.08.20

%% description:
% main function for performing MLE for ODE compartment models describing healthy or malignant hematopoiesis (CHIP, MDS),
% based on experimentally measured cell abundances
%  -    compartments describe cells belonging to a certain cell type which underwent the same number 
%       of divisions dividisions
%  -    parameters describe reaction rates 
%  -    reactions describe proliferation, differentiation and cell death
% function either fits real data or simulates and fits in silico data 
clear;
clc;
close all;

firstIndividual=1; %specify first individual

[opt,nl_end] = getDisorderAnalysisSettings();

if opt.realdata == true
   %% data pre-processing 
   dataPreprocessing(opt);
else
    %% generate in silico data for every specified noise level and individual
    opt = simulateData(opt);
end

for nl_id = 1:nl_end
    if opt.realdata == false
        %% update in silico settings:
        [opt,n_states] = updateInSilicoSettings(nl_id,opt);
    else
        if nl_id==1
            %% get real data settings
            [opt,n_states] = getRealDataSettings(opt);
        end
    end

    %% initialize values:
    [par_min,par_max,CI_lower,CI_upper,PAR_OPT_T,PAR_TEST_T,logL_vec] = initializeParameterResultMatrices(opt);

    for i_ID=firstIndividual:opt.n_individuals %index for individual for which parameter inference is performed

        clearvars -except firstIndividual i_ID opt nl_id nl_end n_states par_min par_max CI_lower CI_upper ...
                          PAR_OPT_T PAR_TEST_T rate_names_opt rate_names_test transformation_str individuals_str...
                          logL_vec theta_test

        [opt] = updatePaths(opt,i_ID);

        if opt.realdata
            %% get experimental data
            data = getExperimentalData(i_ID,opt);
            theta_test = [];
            rate_names_test = [];
        else
            %% load simulated data for current settings:
            [data,theta_test,rate_names_test] = getSimulatedData(opt,i_ID);
        end

        % track the time it takes to run optimization for 1 sample:
        tic;
        t_c = cputime;

        if any(any(isnan(data.NumCellDiv_ALL{1,1})))
           continue; 
        end

        %% update options for parameters
        opt = updateParameterOptions(data,opt);

        %% generate simulation file for model used in optimization
        createSimulationFiles(opt,true,opt.model);

        %% perform MLE optimization
        [parameters,opt,options_par] = performParameterEstimation(opt,theta_test,data,i_ID);

        time_in_s = toc;
        time_cpu_in_s = cputime - t_c;

        %% transform and save parameters, bounds, Confidence intervals
        [par_min,par_max,CI_lower,CI_upper,PAR_OPT_T,PAR_TEST_T,logL_vec] = saveTransformedParameterResult(parameters,par_min,par_max,CI_lower,CI_upper,PAR_OPT_T,PAR_TEST_T,opt.parTransformationStr,opt,theta_test,i_ID,rate_names_test,logL_vec);

        %% observe convergence of optimization:
        MS_percentage = calculateSizeLogLPlateau(parameters);

        %% get analytically estimated noise parameter (in case of hierarchical optimization) 
        [sigma_HO] = getAnalyticallyEstimatedSigma(opt);

        %% save workspace for current individual
        if opt.save
            cd(opt.c_path);
            cd(['./',opt.foldername,'/',opt.subfoldername,'/',opt.subsubfoldername]);
            save(['WS_individual_',opt.individuals{i_ID},'.mat']);
            cd(opt.c_path);
        end

        %% save data for plotting model fit in Python 
        saveModelFitResults(theta_test,parameters.MS.par(:,1),data,opt,n_states,sigma_HO);
    end
end

    function [opt,n_states] = updateInSilicoSettings(nl_id,opt)
        %update opt and simulation files for current model used for fit
        [~,n_states,opt] = getModelParams(opt,opt.model);
        [opt] = getNoiseSettings(opt,opt.noiseLevel{nl_id});
        opt.nL = opt.noiseLevel{nl_id};
    end

    function [opt,n_states] = getRealDataSettings(opt)
        [~,n_states,opt] = getModelParams(opt,opt.model); 
        [opt] = getResultsFolderStrings(opt);
    end

end
    
