% export parameter results to table in word file
% author: Lisa Bast
% date: 29.08.2021
function [Datacell] = export_par_values_to_Word(group_str) 

%% make sure all functions in utils can be used
current_path = cd();
cd('../');
path1 = cd();
cd(current_path);
addpath(genpath([path1,'/utils']));
addpath(genpath([current_path,'/utils']));

%% get list of Individuals
if strcmp(group_str,'MDS')
    individual_IDs = {'620','360', '373','377','227','279','140','135','326','354'};
elseif strcmp(group_str,'healthy age-matched')
    individual_IDs = {'311','312','353','380','559','607','657','791'};
elseif strcmp(group_str,'CHIP')    
    individual_IDs = {'775','552','345','391','560','561','348'};
end

%% go to dir of current individual and extract values
for i = 1:length(individual_IDs)
    clearvars -except individual_IDs i current_path group_str Datacell; 
    cd(['.\results_fit_samples_7divs_3iS_HO_LogNormal_fit_iC\model_union_ABDGI\individual_',num2str(individual_IDs{i})]);
    load(['WS_individual_',num2str(individual_IDs{i}),'.mat'],'opt','parameters','PAR_OPT_T', 'CI_lower', 'CI_upper', 'i_ID');
    if (opt.n_repetitions==1)
        offset = 7;
    else
        offset = 2*7;
    end
    format short g
    par_values_i = num2str(round(PAR_OPT_T(2,:,i_ID),2)');
    CI_l_i = num2str(round(CI_lower(2,:,i_ID),2)');
    CI_u_i = num2str(round(CI_upper(2,:,i_ID),2)');
    
    par_res_i = horzcat(horzcat(horzcat(horzcat(horzcat(par_values_i,repmat(' [',length(parameters.name)-offset,1)),CI_l_i),repmat(', ',length(parameters.name)-offset,1)),CI_u_i),repmat(']',length(parameters.name)-offset,1));
    for i_rates = 1:length(parameters.name)-offset
        if (i==1)
            if i_rates==1
                Datacell=cell(length(parameters.name)-offset+1,length(individual_IDs)+1);
                Datacell{1,1} = 'Parameter';
            end
            Datacell{i_rates+1,1} = format_parameter_str(parameters.name{i_rates+offset});
        end
        Datacell{1,i+1} = num2str(individual_IDs{i});
        Datacell{i_rates+1,i+1} = par_res_i(i_rates,:);
    end
    cd(current_path);
end
% DataCell={'Test 1', num2str(0.3) ,'Pass';
%           'Test 2', num2str(1.8) ,'Fail'};

    function str_latex = format_parameter_str(par_str)
        %currently: a_{HSC_{MEP}}
        %goal: $$a_{HSC \rightarrow MEP}$$
        str_latex = par_str;
        idx = strfind(par_str,'{');
        if ~isempty(idx)
            if length(idx)==2
               par_str(idx(2)-1:idx(2))='!!';
               str_latex = strrep(par_str,'!!',' \rightarrow ');
               idx = strfind(str_latex,'}');
               str_latex(idx(2))='$';
               str_latex = ['$$',str_latex,'$'];
            else
               str_latex = ['$$',str_latex,'$$'];
            end
        end
    end

end
