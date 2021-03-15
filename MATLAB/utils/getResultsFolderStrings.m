function [opt] = getResultsFolderStrings(opt)

%opt.foldername and opt.subfoldername are changed in case option is set to
%initialize

%j_sim: model scheme used for simulations index
%j: model scheme used for fit index

HO_str = '';
if strwcmp(opt.optimizationMode,'hierarchical')
    HO_str = '_HO';
end        
if opt.realdata==false && strcmp(opt.RUN,'in_silico')
    app_str = '_test';
else
    app_str = '_fit_samples';
end
opt.foldername = ['results',app_str,'_',num2str(opt.n_divStates),'divs_',num2str(opt.n_intermediateStates(opt.iS_ID)),'iS',HO_str,'_',opt.noiseType];


if strcmp(opt.RUN,'in_silico')
    opt.foldername = [opt.foldername,'_simulatedFrom_',opt.model_sim];
end

if opt.fitInitialConds && ~strwcmp(opt.foldername,'*_fit_iC*')
   opt.foldername = [opt.foldername,'_fit_iC'];  
end
opt.subfoldername = [opt.model];


end