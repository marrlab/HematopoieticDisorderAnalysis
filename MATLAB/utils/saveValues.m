function [] = saveValues(opt_RUN,opt_group,bool_fit_repetitions_seperately,n_is,individual_IDs,sim_model_str,opt_model_str,noise_level)

% opt_RUN = 'fit_samples';%'hierarchy_comparison_BIC'
% opt_group = 'healthy';%'MDS'
% bool_fit_repetitions_seperately = true;
% bool_realdata=false;

fileName = '2019_07_data.xlsx';

cd('../../')
path1 = cd();
addpath(genpath([path1,'/Tools/Hematopoiesis']));
cd('./AnalysisAndModeling/BulkAnalysis/')
current_dir = cd();
 
if strcmp(opt_RUN,'test_inference_procedure')
    path=[current_dir,'/Healthy_MDS_Comparison/Parameter_Inference/'];
    noiselevel_str = strjoin(strcat(noise_level,'_'));
    noiselevel_str = noiselevel_str(noiselevel_str ~= ' ');
    ResultsFolderName = ['results_test_inference_procedure_7divs_',num2str(n_is),'iS_HO_LogNormal_',noiselevel_str(1:end-1),'_fit_iC'];
    disp(ResultsFolderName)
    cd(path);
    for sm_id = 1:length(sim_model_str)
        clearvars PAR_TEST_T individuals_str theta_test rate_names_test
        for om_id = 1: length(opt_model_str)
            clearvars -except g_id sm_id om_id current_dir group_str sim_model_str opt_model_str individual_IDs path...
                              theta_test rate_names_test PAR_TEST_T individuals_str n_is ResultsFolderName noise_level opt_group
            par_min=[];
            par_max = [];
            CI_lower = [];
            CI_upper = [];
            PAR_OPT_T = [];
            PAR_TEST_T = [];
            for nl_id = 1:length(noise_level)
                for i_id = 1:length(individual_IDs)
                    target_dir = [ResultsFolderName,'/',opt_model_str{om_id},'_model/individual_',individual_IDs{i_id},'_',noise_level{nl_id},'_noise'];
                    cd(target_dir)
                    if om_id==1
                        load(['WS_',opt_group,'_individual_',individual_IDs{i_id}],'parameters','opt','transformation_str','theta_test','rate_names_test','individuals_str');
                        rate_names_opt = rate_names_test;
                        cd(path);
                        if (i_id==1)
                            p_min = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                            p_max = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                            ci_lower = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                            ci_upper = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                            Par_OPT_T = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                            Par_TEST_T = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                        end
                        [p_min, p_max, ci_lower, ci_upper, Par_OPT_T, Par_TEST_T]  = saveTransformedParResult(parameters,p_min,p_max,ci_lower,ci_upper,individual_IDs,Par_OPT_T,Par_TEST_T,transformation_str,opt,theta_test,i_id,rate_names_test);
                    else
                        load(['WS_',opt_group,'_individual_',individual_IDs{i_id}],'parameters','opt','transformation_str');
                        cd(path);
                        [p_min, p_max, ci_lower, ci_upper, Par_OPT_T, Par_TEST_T]  = saveTransformedParResult(parameters,p_min,p_max,ci_lower,ci_upper,individual_IDs,Par_OPT_T,Par_TEST_T,transformation_str,opt,theta_test,i_id,rate_names_test);
                    end
                    if i_id==length(individual_IDs)
                        par_min = cat(3,par_min, p_min);
                        par_max = cat(3,par_max, p_max);
                        CI_lower = cat(3,CI_lower, ci_lower);
                        CI_upper = cat(3,CI_upper, ci_upper);
                        PAR_OPT_T = cat(3,PAR_OPT_T, Par_OPT_T);
                        PAR_TEST_T = cat(3,PAR_TEST_T, Par_TEST_T);
                        if nl_id == length(noise_level) 
                            cd(['./',opt.foldername,'/',opt.subfoldername,'/',opt.subsubfoldername]);
                            save(['ws_parameters_',opt_group,'.mat'],'par_min','par_max','CI_lower','CI_upper','PAR_OPT_T','PAR_TEST_T','rate_names_opt','rate_names_test','transformation_str','individuals_str');
                            cd(path);
                        end
                    end
                end
            end
        end
    end
 else
    switch opt_RUN
        case 'fit_samples'
            ResultsFolderName = ['results_fit_samples_7divs_',num2str(n_is),'iS_HO_LogNormal_fit_iC'];
            path=[current_dir,'/Healthy_MDS_Comparison/Parameter_Inference/'];
        case 'hierarchy_comparison_BIC'
            ResultsFolderName = ['results_hierarchy_comparison_BIC_7divs_',num2str(n_is),'iS_HO_LogNormal_fit_iC'];
            path=[current_dir,'/Lineage_Hierarchy_Comparison_preAnalysis/Model_Selection/'];
    end
    cd(path)
    group_str = {'healthy','MDS'};

    if bool_fit_repetitions_seperately==true
        add_str_fit_repetitions_seperately = '_rep_sep';
    else
        add_str_fit_repetitions_seperately = '';
    end

    opt_model_str = {'model_A','model_B','model_C','model_D','model_E','model_F','model_G','model_H','model_I','model_J'};
    for g_id = 1:length(group_str)
        individuals_str_simple = individual_IDs; 
        clearvars PAR_TEST_T theta_test rate_names_test
        for om_id = 1:length(opt_model_str)
            clearvars -except g_id sm_id om_id current_dir group_str sim_model_str opt_model_str...
                              theta_test rate_names_test PAR_TEST_T individuals_str_simple individuals_str...
                              fileName ResultsFolderName add_str_fit_repetitions_seperately bool_fit_repetitions_seperately
            for i_id = 1:length(individuals_str_simple)
                target_dir = ['./',ResultsFolderName,'/',opt_model_str{om_id},'_model/individual_',individuals_str_simple{i_id}];
                cd(target_dir)
                if om_id==1
                    load(['WS_',group_str{g_id},'_individual_',individuals_str_simple{i_id}],'parameters','opt','transformation_str','theta_test','rate_names_opt');
                    cd(path);                
                    opt.individuals = individuals_str_simple;
                    opt.n_individuals = length(individuals_str_simple);
                    if (i_id==1)
                        par_min = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                        par_max = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                        CI_lower = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                        CI_upper = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                        PAR_OPT_T = zeros(length(transformation_str),length(opt.rates(~strwcmp(opt.rates,'x0_*'))),opt.n_individuals);
                    end
                    [par_min, par_max, CI_lower, CI_upper, PAR_OPT_T, ~]  = saveTransformedParResult(parameters,par_min,par_max,CI_lower,CI_upper,individual_IDs,PAR_OPT_T,[],transformation_str,opt,[],i_id,rate_names_opt);
                else
                    load(['WS_',group_str{g_id},'_individual_',individuals_str{i_id}],'parameters','opt','transformation_str');
                    cd(path);
                    [par_min, par_max, CI_lower, CI_upper, PAR_OPT_T, ~] = saveTransformedParResult(parameters,par_min,par_max,CI_lower,CI_upper,individual_IDs,PAR_OPT_T,[],transformation_str{ts_ID},opt,[],i_ID,rate_names_opt);
                end
                if i_id==length(individuals_str_simple)
                    individuals_str = individuals_str_simple;
                    cd(target_dir);
                    save(['ws_parameters_',opt.group,add_str_fit_repetitions_seperately,'.mat'],'par_min','par_max','CI_lower','CI_upper','PAR_OPT_T','PAR_TEST_T','rate_names_opt','rate_names_test','transformation_str','individuals_str');
                    cd(path);
                end

            end
        end
    end
end

cd(path)
% end