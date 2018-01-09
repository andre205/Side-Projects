%shift radon values according to apparent recalibration dates

%number of times filtering process is repeated
loop_count = 10;

%value cutoff (applied immediately after reading raw data)
value_cutoff_max = 80000;
value_cutoff_min = 0;

%smallest running average difference that indicates a recalibration
threshhold = 1500;

%running average verification for true break in months
%MAX 3 MONTHS
verification_time = 2;

%raw unmodified input file
%input_file = fopen('jan15-jan17.csv');
input_file = fopen('5year_raw.csv');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


all_data = textscan(input_file,'%s%s%f','delimiter',',');
dates = all_data{1};
times = all_data{2};
values = all_data{3};
modifiedvalues = all_data{3};
formatIn = 'dd/mm/yyyy';
datenums = datenum(dates,formatIn);
%modified later for break indication
breaks = all_data{3};

for i = 1:size(modifiedvalues)
%HARD THRESHHOLD APPLIED IMMEDIATELY
	if (modifiedvalues(i) > value_cutoff_max)
		values(i) = NaN;
		modifiedvalues(i) = NaN;
	elseif (modifiedvalues(i) < value_cutoff_min)
		values(i) = NaN;
		modifiedvalues(i) = NaN;
	end
end

for loop = 1:1:loop_count
	disp('---------------------------');
	disp(['FILTER ',num2str(loop)]);

	for i = 1:1:size(breaks)
		breaks(i) = NaN;
	end

	breaksum = 0;
	break_intermediate_array = {};
	break_intermediate_array2 = {};

	for i = 24:1:size(modifiedvalues)-24

		%start at 24th hour in the data
		%check 24 hours after point and 24 hours before point,
		%compare both and add to intermediate array1 if difference between averages > threshhold
		temp24avg1 = 0;
		temp24sum1 = 0;
		tempcounter1 = 0;
		for j = 0:1:23
			if modifiedvalues(i+j) > 0
				temp24sum1 = temp24sum1 + modifiedvalues(i+j);
				tempcounter1 = tempcounter1 + 1;
			end
		end
		temp24avg1 = temp24sum1/tempcounter1;

		temp24avg2 = 0;
		temp24sum2 = 0;
		tempcounter2 = 0;
		for j = 0:1:23
			if modifiedvalues(i-j) > 0
				temp24sum2 = temp24sum2 + modifiedvalues(i-j);
				tempcounter2 = tempcounter2 + 1;
			end
		end
		temp24avg2 = temp24sum2/tempcounter2;

		if temp24avg2-temp24avg1 > threshhold || temp24avg2-temp24avg1 < -threshhold
			%disp(i)
			break_intermediate_array = [break_intermediate_array, i];
			breaksum=breaksum+1;
		end


		%{
		ONE HOUR DIFFERENCE OUTPUT
		if (values(i) - values(i-1) > threshhold)
			x1 = dates(i);
			x2 = times(i);
			x3 = values(i-1);
			x4 = values(i);
			x5 = x3-x4;
			y = ['INCREASE',x1, x2, x3, x4, 'difference:',x5,'row:',i];
			disp(y)
		end

		if (values(i-1) - values(i) > threshhold)
			x1 = dates(i);
			x2 = times(i);
			x3 = values(i-1);
			x4 = values(i);
			x5 = x3-x4;
			y = ['DECREASE',x1, x2, x3, x4, 'difference:',x5,'row:',i];
			disp(y)
		end

		%}

	end



	%display number of potential points of breaks + anomolies
	%disp('breaks + anoms');
	%disp(breaksum);

	%transpose array and change to integer values for easier parsing
	breaksum = 0;
	break_intermediate_array = break_intermediate_array';
	break_intermediate_array = cell2mat(break_intermediate_array);

	%check 1 month * (verification_time) before and after each potential break for confirmation of a persistent change in avg value
	for k = 1:1:size(break_intermediate_array)
		test_value = break_intermediate_array(k);
		temp_mo_avg1 = 0;
		temp_mo_sum1 = 0;
		tempcounter1 = 0;
		for j = 0:1:round(verification_time*730)
			if modifiedvalues(test_value+j) > 0
				temp_mo_sum1 = temp_mo_sum1 + modifiedvalues(test_value+j);
				tempcounter1 = tempcounter1 + 1;
			end
		end
		temp_mo_avg1 = temp_mo_sum1/tempcounter1;

		temp_mo_avg2 = 0;
		temp_mo_sum2 = 0;
		tempcounter2 = 0;
		for j = 0:1:round(verification_time*730)
			if modifiedvalues(test_value-j) > 0
				temp_mo_sum2 = temp_mo_sum2 + modifiedvalues(test_value-j);
				tempcounter2 = tempcounter2 + 1;
			end
		end
		temp_mo_avg2 = temp_mo_sum2/tempcounter2;

		if temp_mo_avg2-temp_mo_avg1 > threshhold || temp_mo_avg2-temp_mo_avg1 < -threshhold
			break_intermediate_array2 = [break_intermediate_array2, test_value];
			breaksum=breaksum+1;
		end
	end

	%display (ideally) number of potential points of breaks ONLY
	%disp('breaks only');
	%disp(breaksum);


	%if values in final array are adjacent (representing the same potential break, find the median and use that instead

	%invert break matrix for easier cell reference
	break_intermediate_array2 = break_intermediate_array2';
	break_intermediate_array2 = cell2mat(break_intermediate_array2);

	%generate array containing number of adjacent cells representing same break point
	break_adjacency_array = {};
	temp_count = 0;

	i2_size_matrix = size(break_intermediate_array2);
	i2_size = i2_size_matrix(1);

	if i2_size > 1

		prev_k = break_intermediate_array2(1);

		for k = 2:1:i2_size

			if break_intermediate_array2(k) == prev_k + 1
				temp_count = temp_count + 1;
			else
				break_adjacency_array = [break_adjacency_array, temp_count];
				temp_count = 0;
			end

			if k == i2_size
				break_adjacency_array = [break_adjacency_array, temp_count];
				temp_count = 0;

			end

			prev_k = break_intermediate_array2(k);
		end
	else
		disp('NO ADJACENT BREAK POINTS');
	end

	%simplify break array to single points
	%using numbers in adj array, avg that many pts from intermediate array2 to find value to put in final array

	break_adjacency_array = break_adjacency_array';
	break_adjacency_array = cell2mat(break_adjacency_array);

	break_final_array = {};
	break_array_counter = 1;

	if size(break_adjacency_array) > 0

		for p = 1:1:size(break_adjacency_array)
			t_a = 0;
			t_c = 0;

			for q = 1:1:break_adjacency_array(p)
				t_a = t_a + break_intermediate_array2(break_array_counter);
				break_array_counter = break_array_counter + 1;
			end
			%for all points representing same break, find avg and round to nearest int - append to final break point array
			break_array_counter = break_array_counter + 1;
			t_a = t_a/break_adjacency_array(p);
			t_a = round(t_a);
			disp(t_a);
			if t_a > 0
				break_final_array = [break_final_array, t_a];
			end
		end
	else
		disp('BREAK ADJACENCY ARRAY EMPTY');
	end

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%		 DATA CORRECTION   			%
	%    (populating modifiedvalues array for plotting	%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	%visit each break in final array and shift values on RIGHT
	%to match 1 month running average of values on LEFT

	break_final_array = cell2mat(break_final_array);

	t_c1 = 0;
	t_c2 = 0;
	mo_avg1 = 0;
	mo_avg2 = 0;
	break_point = 0;

	final_array_size_matrix = size(break_final_array);
	final_array_size = final_array_size_matrix(2);

	if final_array_size > 0

		for f = 1:1:final_array_size
			break_point = break_final_array(f);
			if f == final_array_size
				next_break_point = size(modifiedvalues);
			else
				next_break_point = break_final_array(f+1);
			end

			t_c1 = 0;
			t_c2 = 0;
			mo_avg1 = 0;
			mo_avg2 = 0;

			%potentially bad to use verification time here, verify later
			for j = 0:1:round(verification_time*730)
				if modifiedvalues(break_point+j) > 0
					mo_avg1 = mo_avg1 + modifiedvalues(break_point+j);
					t_c1 = t_c1 + 1;
				end

				if modifiedvalues(break_point-j) > 0
					mo_avg2 = mo_avg2 + modifiedvalues(break_point-j);
					t_c2 = t_c2 + 1;
				end
			end
			mo_avg1 = mo_avg1/t_c1;
			mo_avg2 = mo_avg2/t_c2;
			%disp(mo_avg1);
			%disp(mo_avg2);

			%right higher than left = shift right down
			if mo_avg2 > mo_avg1
				shift = mo_avg2 - mo_avg1;
				%for j = break_point:1:break_point+730
				for j = break_point:1:next_break_point

					if modifiedvalues(j) > 0
						modifiedvalues(j) = modifiedvalues(j) + shift;
					end
				end
			end

			%left higher than right = shift right up
			if mo_avg2 < mo_avg1
				shift = mo_avg1 - mo_avg2;
				%for j = break_point:1:break_point+730
				for j = break_point:1:next_break_point

					if modifiedvalues(j) > 0
						modifiedvalues(j) = modifiedvalues(j) - shift;
					end
				end
			end
		end

		%BREAK MARKERS
		disp('BREAKS')
		disp(final_array_size);
		for f = 1:1:final_array_size
			for g = 0:1:20
				breaks(break_final_array(f)+g) = 61500-g*30;
			end
		end
	else
		disp('NO BREAKS FOUND - EXITING LOOP');
		loop = loop_count;
		break;
	end


	%{
	for i = 2:size(modifiedvalues)
	%FINAL CLEANUP REMOVE LATER
		if (modifiedvalues(i) - modifiedvalues(i-1) > 8000)
			modifiedvalues(i) = modifiedvalues(i-1);
		elseif (modifiedvalues(i) - modifiedvalues(i-1) < -8000)
			modifiedvalues(i) = modifiedvalues(i-1);
		end
	end
	%}



	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%		     OUTPUT		%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


	%{
	output_img_all = figure('visible','off');
	plot(datenums,values,'b');
	%hold on
	%plot(datenums,modifiedvalues);
	%legend('show','Raw values','Corrected values');


	xlabel('Date');
	%datetick('x','mmm yyyy');
	NumXTicks = 12;
	L = get(gca,'XLim');
	set(gca,'XTick',linspace(L(1),L(2),NumXTicks));
	L = get(gca,'YLim');
	L(2) = L(2)/1000 - 1;
	L(2) = L(2) * 1000;
	NumYTicks = (L(2)-L(1))/1000 + 1;
	%NumYTicks = 40;
	set(gca,'YTick',linspace(L(1),L(2),NumYTicks));

	%for dd/mm/yyyy x tick format
	%datetick('x',formatIn, 'keepticks');
	%for mon/yyyy format

	datetick('x','mmm yyyy', 'keepticks');
	ylabel('Counting Rate');
	title('Orange Gamma Sensor');
	grid on
	%grid minor
	saveas(output_img_all,'Orange_Gamma_5_year_raw_values_treshhold_80k','png');
	%}


	output_img_all = figure('visible','off');
	plot(datenums,values,'r');
	hold on
	plot(datenums,modifiedvalues,'b');
	hold on
	plot(datenums,breaks,'m','LineWidth',1.5);
	legend('show','Raw values','Corrected values',[num2str(final_array_size),' Identified Breaks']);


	xlabel('Date');
	%datetick('x','mmm yyyy');
	NumXTicks = 15;
	L = get(gca,'XLim');
	set(gca,'XTick',linspace(L(1),L(2),NumXTicks));
	L = get(gca,'YLim');
	L(2) = L(2)/1000 - 1;
	L(2) = L(2) * 1000;
	NumYTicks = (L(2)-L(1))/1000 + 1;
	%NumYTicks = 40;
	set(gca,'YTick',linspace(L(1),L(2),NumYTicks));

	%for dd/mm/yyyy x tick format
	%datetick('x',formatIn, 'keepticks');
	%for mon/yyyy format

	datetick('x','mm/yy', 'keepticks');
	ylabel('Counting Rate');
	title(['5 Year Orange Gamma Plot - Corrected Values - Break Detection Threshhold: ', num2str(threshhold)]);
	grid on
	%grid minor
	saveas(output_img_all,['TESTING2/filter_image_',num2str(loop)],'png');

end

%WRITE FINAL CSV HERE
