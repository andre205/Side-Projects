input_file = fopen('orangegamma-jan15-jan17.csv');

all_data = textscan(input_file,'%s%s%f','delimiter',',');

dates = all_data{1};
times = all_data{2};
values = all_data{3};


formatIn = 'dd/mm/yyyy';
datenums = datenum(dates,formatIn);



sumvalues = 0;
counter = 1;
for i = 1:24:size(values)-24
	sumvalues = 0;
	sumdates = 0;

	valmean = 0;
	datemean = 0;	

	for j = 1:24
		sumvalues = sumvalues + values(i+j);
		sumdates = sumdates + datenums(i+j);
	end
	valmean = sumvalues/24;
	datemean = sumdates/24;

	avgvalues(counter) = valmean;
	avgdatenums(counter) = datemean;
	
	counter=counter+1;
end



%alternative running average filter
windowsize = 24;
b = (1/windowsize)*ones(1,windowsize);
a = 1;
y = filter(b,a,values);

fclose(input_file);

output_img_all = figure('visible','off');
plot(datenums,values);

xlabel('Date');
%datetick('x','mmm yyyy');

NumXTicks = 12;
L = get(gca,'XLim');
set(gca,'XTick',linspace(L(1),L(2),NumXTicks));


L = get(gca,'YLim');
L(2) = L(2)/1000 - 1;
L(2) = L(2) * 1000;
NumYTicks = (L(2)-L(1))/1000 + 1;
set(gca,'YTick',linspace(L(1),L(2),NumYTicks));


%for dd/mm/yyyy x tick format
%datetick('x',formatIn, 'keepticks');

%for mon/yyyy format
datetick('x','mmm yyyy', 'keepticks');



ylabel('Counting Rate');
title('Orange Gamma Sensor');
grid on
%grid minor

saveas(output_img_all,'Orange_Gamma_15-17','png');



output_img_avg = figure('visible','off');
plot(avgdatenums,avgvalues);
xlabel('Date');
NumXTicks = 12;
L = get(gca,'XLim');
set(gca,'XTick',linspace(L(1),L(2),NumXTicks));
L = get(gca,'YLim');
L(2) = L(2)/1000 - 1;
L(2) = L(2) * 1000;
NumYTicks = (L(2)-L(1))/1000 + 1;
set(gca,'YTick',linspace(L(1),L(2),NumYTicks));
datetick('x','mmm yyyy', 'keepticks');
ylabel('Counting Rate');
title('Orange Gamma Sensor');
grid on
%grid minor

saveas(output_img_avg,'Orange_Gamma_15-17_24hr_Running_Avg','png');

output_img_avg = figure('visible','off');
plot(datenums,y);
xlabel('Date');
NumXTicks = 12;
L = get(gca,'XLim');
set(gca,'XTick',linspace(L(1),L(2),NumXTicks));
L = get(gca,'YLim');
L(2) = L(2)/1000 - 1;
L(2) = L(2) * 1000;
NumYTicks = (L(2)-L(1))/1000 + 1;
set(gca,'YTick',linspace(L(1),L(2),NumYTicks));
datetick('x','mmm yyyy', 'keepticks');
ylabel('Counting Rate');
title('Orange Gamma Sensor');
grid on
%grid minor

saveas(output_img_avg,'Orange_Gamma_15-17_Combined_Plot','png');


