function [individuals,dataSet] = getIndividuals(fileName,group,bool_fit_repetitions_seperately)

individuals=[];
dataSet=[];

%% create table from data sheet
cd('./data')
DT = readtable(fileName,'Sheet','ready4MATLAB','TreatAsEmpty','-');

%% sort rows in Table by age
DataTable = sortrows(DT,'Alter'); %column does not exist anymore

%% get rid of empty lines
toDelete = strcmp(DataTable.filename,'0');
DataTable(toDelete,:)=[];

%% add column repetition
f_str = cellfun(@(x) x(1:end-6), DataTable.filename, 'un', 0);
Fnames=f_str;
Fnames_uni = unique(f_str,'stable');
for i = 1:length(f_str)
    f_str{i}(regexp(f_str{i},'[a-z]+'))='';
end
sampleNums = cellfun(@(x) x(max([regexp(x,'[H]'),regexp(x,'[MDS]')])+1:end), f_str, 'un', 0);
sampleNums_uni = unique(sampleNums,'stable');

%sampleIDs_uni = unique(cellfun(@(x) x(max([regexp(x,'[H]'),regexp(x,'[MDS]')])+1:end), Fnames_uni, 'un', 0),'stable');
DataTable.repetition = ones(size(DataTable,1),1);
DataTable.replicate = ones(size(DataTable,1),1);
for j=1:length(sampleNums_uni)
    idx_Fn = find(cellfun(@(x) strwcmp(x(9:end),['*',sampleNums_uni{j},'*']), Fnames_uni));
    %whenever length(idx_Fn)>1: more than 1 replicate and/or repetition
    %idx_sID = find(strwcmp(sampleIDs_uni,['*',sampleNums_uni{j},'*']));
    %whenever length(idx_Fn)>length(idx_sID) %more than 1 replicate
    counter_repe=1;
    timestamp = '';
    bools = [true true true];
    for k1=1:length(idx_Fn)
        %repetition: unique time stamp or sampleIDs occur with 'a' and ''
        %ending
        idx_DT = find(strwcmp(DataTable.filename,[Fnames_uni{idx_Fn(k1)},'*']));
        idx_a = find(strwcmp(Fnames_uni{idx_Fn(k1)},'*a*'));
        idx_b = find(strwcmp(Fnames_uni{idx_Fn(k1)},'*b*'));
        DataTable.repetition(idx_DT) = counter_repe.*ones(size(idx_DT));
        if ~isempty(idx_b)
            DataTable.replicate(idx_DT) = 2.*ones(size(idx_DT));
            bools(3)=false;
        else
            DataTable.replicate(idx_DT) = ones(size(idx_DT));
            if ~isempty(idx_a)
                bools(2)=false;
            else
                bools(1)=false;
            end
        end
        if (~strcmp(Fnames_uni{idx_Fn(k1)},timestamp) && bools(1)==false && isempty(idx_a) && isempty(idx_b)|| sum(bools(2:3)==false)==2)
            counter_repe = counter_repe+1;
            %update timestamp
            timestamp = Fnames_uni{idx_Fn(k1)}(1:8);
        end
    end
end
sampleNames_selection = cellfun(@(x) x(max([regexp(x,'[H]'),regexp(x,'[MDS]')])+1:end), f_str(find(strcmp(DataTable.Gruppe_2_categories,group))), 'un', 0);
if bool_fit_repetitions_seperately
    sampleNames_all = cellfun(@(x) x(max([regexp(x,'[H]'),regexp(x,'[MDS]')])+1:end), f_str, 'un', 0);
    for l=1:length(Fnames)
        switch Fnames{l}(end)
            case {'a','b'}
                add_str{l} = Fnames{l}(end);
            otherwise
                add_str{l} = '';
        end
    end
    DataTable.sample_name = strcat(strcat(sampleNames_all,strcat('_',num2str(DataTable.repetition))),add_str');
    I=unique(strcat(sampleNames_selection,strcat('_',num2str(DataTable.repetition(find(strcmp(DataTable.Gruppe_2_categories,group)))))),'stable');
else
    %% add column sample_name
    %filename: Datum des Sorttages; Probennummer (H fuer healty, M fuer MDS); a,b oder c bei Doppel- bzw. Dreifachbestimmungen; geerntet an Tag X
    I=[];
    
    idx_end = strfind(DataTable.filename,'.');
    idx=[];

    for i=1:size(DataTable,1)
        idx_start_MDS = strfind(DataTable.filename{i},'S');
        idx_start_H = strfind(DataTable.filename{i},'H');
        if ~isempty(idx_start_MDS)
            idx_start{i}=idx_start_MDS;
        else
            idx_start{i}=idx_start_H;
        end
        %if strcmp(DataTable.Gruppe_2_categories{i},group)
        sampleName = DataTable.filename{i}(idx_start{i}+1:idx_end{i}-1);
        idx_T=strfind(sampleName,'T');
        lastPart = sampleName(idx_T:end);
        lastPart_red = lastPart(isletter(sampleName(idx_T:end)));
        lastPart_red(strfind(lastPart_red,'T')) =[];
        DataTable.sample_name{i} = strcat(sampleName(1:idx_T-1),lastPart_red);
        if strcmp(DataTable.Gruppe_2_categories{i},group)
            idx = [idx, i];
        end
    end
    if ~isempty(idx_start)
        I = unique(DataTable.sample_name(idx),'stable');
        for i=1:length(I)
            tbd = regexp(I{i},'[a-z]+');
            if ~isempty(tbd)
               I{i}(tbd)=[]; %get rid of letter in sample name indicating replicate
            end
        end
        I=unique(I,'stable');
    end
end
I(strwcmp(I,'450*') | strwcmp(I,'425*') | strwcmp(I,'729*') | strwcmp(I,'754*') | strwcmp(I,'215*') | strwcmp(I,'433*') | strwcmp(I,'173*') | strwcmp(I,'110*') |  strwcmp(I,'460*') | strwcmp(I,'592*') | strwcmp(I,'545*'))=[]; %too few cell counts
%I(strwcmp(I,'439*') | strwcmp(I,'547*') | strwcmp(I,'482*') | strwcmp(I,'522*') | strwcmp(I,'370*') | strwcmp(I,'353*') | strwcmp(I,'311*') | strwcmp(I,'380*') | strwcmp(I,'312_2') |strwcmp(I,'559*'))=[]; %already fitted
individuals=[individuals;I];
dataSet=[dataSet; ones(length(I),1)];

%% add column experimentalDesign
DataTable.experimentalDesign = ones(size(DataTable,1),1);

save('Data.mat','DataTable')
cd('../')
end