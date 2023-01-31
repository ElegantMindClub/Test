
currentFolder = pwd;
filename = "/Users/Mingda/Downloads/data/asdf_2023-01-31_11h31.01.051.csv";

results = readtable(filename);

% gets correct reaction times
rt_seconds = results{results.('isCorrect')==1,{'reactionTime'}};
rt_ms = rt_seconds * 1000;
rt_no_outliers = rmoutliers(rt_ms, 'quartiles');

% calculate things
mean_rt = mean(rt_no_outliers);
std_dev = std(rt_no_outliers);

% create figure
figure(1);
set(gcf,'Position',[300,100,550,400]);
set(gca,'Position',[0.13 0.11 0.7 0.815]);

%Create a histogram of Reaction Time (ms) vs Frequency, with outliers removed
% , 'Normalization','Probability', 'FaceColor',testcolor,'EdgeColor',outlinecolor)
H = histogram(rt_no_outliers, 'BinWidth', 100); 
xlabel('Reaction Time (ms)');
ylabel('Frequency (Normalized to Probability)');
title('RT Histogram');
box off;

% set axes lengths
handle = gca;
textheight_y = handle.YLim(2) - handle.YLim(1);
textheight_x = handle.XLim(2) - handle.XLim(1);

% write mean
annotation('textbox', [0.83,0.75,0.5,0],'string',sprintf('Mean: %0.2f\nSD: %0.2f', mean_rt,std_dev),'EdgeColor','none');

%Save graph to folder
%saveas(gcf,'SingleColor_' + testcolor + '_Normalized_' + subjectname + '.png')