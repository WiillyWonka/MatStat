
clear;
clc;
clf;

C = 400; %nm
filename = 'depz.txt';
RELdeposition_coords_map_z = rot90(dlmread(filename, '', 1, 0),3);
row_dep = max(RELdeposition_coords_map_z(:));
deposition_coords_map_z = C * (RELdeposition_coords_map_z./row_dep);


%%%%INPUTS%%%%

deposition_offset_x = -145; % mm
deposition_offset_y = -145; % mm
deposition_len_x = 290; % mm
deposition_len_y = 290; % mm
deposition_res_x = 1; % 1/mm
deposition_res_y = 1; % 1/mm

alpha0_sub = 0*pi;
R = 90;                     %radius of the planet orbit, mm

k_input = [6, 15, 25, 40, 55];
NR_input  = [12, 18, 24, 28, 35];

%%%%%%%

substrate_diameter = 90; % Substrate width, mm

substrate_x_res = 10; % Substrate x resolution, mm
substrate_y_res = 10; % Substrate y resolution, mm

substrate_coords_x = R-substrate_diameter/2:substrate_diameter/substrate_x_res:R+substrate_diameter/2;
substrate_coords_y = -substrate_diameter/2:substrate_diameter/substrate_y_res:substrate_diameter/2;

%%%% depoition profile meshing
deposition_coords_x = deposition_offset_x:deposition_res_x:deposition_offset_x+deposition_len_x-1;
deposition_coords_y = deposition_offset_y:deposition_res_y:deposition_offset_y+deposition_len_y-1;
[deposition_coords_map_x, deposition_coords_map_y] = meshgrid(deposition_coords_x, deposition_coords_y);

%%%% plot deposition area and holder circles
ang=0:0.01:2*pi;
deltat = ang(2)./(2*pi);

[substrate_coords_map_x, substrate_coords_map_y] = meshgrid(substrate_coords_x, substrate_coords_y);


 for i = 1:size(substrate_coords_map_x, 1)
    for j = 1:size(substrate_coords_map_x, 2)
        if sqrt((substrate_coords_map_x(i, j)-R).^2+substrate_coords_map_y(i, j).^2) > substrate_diameter/2
            substrate_coords_map_x(i, j) = NaN;
            substrate_coords_map_y(i, j) = NaN;
        end
    end
 end

k_input_len = length(k_input);
NR_input_len = length(NR_input);

I_var = zeros([k_input_len, NR_input_len]);

%%%%SEARCHING VARIANCE OF SPRAING INTECITY FOR ALL INPUT VALUES %%%%

for k_idx = 1:k_input_len
    k = k_input(k_idx);
    for NR_idx = 1:NR_input_len
        NR = NR_input(NR_idx);

        a = 0:2*pi/300:NR*2*pi;     %anglural position of the planet in its orbit

        %%%%%%
        rho = zeros(size(substrate_coords_map_x));
        alpha0 = zeros(size(substrate_coords_map_x));
        xp = zeros([size(substrate_coords_map_x) numel(a)]);
        yp = zeros([size(substrate_coords_map_x) numel(a)]);
        z = zeros([size(substrate_coords_map_x) numel(a)]);
        rel_th = zeros(1);
        I = zeros([size(substrate_coords_map_x)]);

        %gridded interpolant
        F = griddedInterpolant(deposition_coords_map_x', deposition_coords_map_y', deposition_coords_map_z');

        for i = 1:size(substrate_coords_map_x, 1)
            for j = 1:size(substrate_coords_map_x, 2)
                if substrate_coords_map_x(1, j) >= R
                    rho(i, j) = sqrt(abs(substrate_coords_map_x(i, j)-R).^2 + substrate_coords_map_y(i, j).^2);
                else
                    rho(i, j) = -sqrt(abs(substrate_coords_map_x(i, j)-R).^2 + substrate_coords_map_y(i, j).^2);
                end

                if i == round((substrate_y_res+1)/2) && j == round((substrate_x_res+1)/2)
                    alpha0(i, j) = 0;
                else
                    alpha0(i, j) = asin(substrate_coords_map_y(i, j) / rho(i, j));
                end
                %Drawing path
                for ii = 1:length(a)
                    xp(i, j, ii) = R*cos(a(ii)+alpha0_sub)+rho(i, j)*cos(a(ii)*k + alpha0(i, j));
                    yp(i, j, ii) = R*sin(a(ii)+alpha0_sub)+rho(i, j)*sin(a(ii)*k + alpha0(i, j));
                    z(i, j, ii) =  F(xp(i, j, ii), yp(i, j, ii)); %get value z for xp, yp
                    rel_th = 0;
                end
                for jj = 1:length(a)
                    if jj > 1
                        rel_th = rel_th + (z(i, j, jj-1) + z(i, j, jj))/2;
                    else
                        rel_th = rel_th + z(i, j, jj);
                    end
                end
                I(i,j) = rel_th * deltat;
            end
        end

        I_var(k_idx, NR_idx)  = var(I(:),'omitnan');
    end

end

%%%%%%


%find optimum
[min_var, indexes] = min(I_var(:)); 
[k_idx, NR_idx] = ind2sub(size(I_var), indexes);
k_optim = k_input(k_idx);
NR_optim = NR_input(NR_idx);

a = 0:2*pi/300:NR*2*pi;     %anglural position of the planet in its orbit
rho = zeros(size(substrate_coords_map_x));
alpha0 = zeros(size(substrate_coords_map_x));
xp = zeros([size(substrate_coords_map_x) numel(a)]);
yp = zeros([size(substrate_coords_map_x) numel(a)]);
z = zeros([size(substrate_coords_map_x) numel(a)]);
rel_th = zeros(1);
I = zeros(size(substrate_coords_map_x));

%gridded interpolant
F = griddedInterpolant(deposition_coords_map_x', deposition_coords_map_y', deposition_coords_map_z');

k = k_optim;
NR = NR_optim;

for i = 1:size(substrate_coords_map_x, 1)
    for j = 1:size(substrate_coords_map_x, 2)
        if substrate_coords_map_x(1, j) >= R
            rho(i, j) = sqrt(abs(substrate_coords_map_x(i, j)-R).^2 + substrate_coords_map_y(i, j).^2);
        else
            rho(i, j) = -sqrt(abs(substrate_coords_map_x(i, j)-R).^2 + substrate_coords_map_y(i, j).^2);
        end

        if i == round((substrate_y_res+1)/2) && j == round((substrate_x_res+1)/2)
            alpha0(i, j) = 0;
        else
            alpha0(i, j) = asin(substrate_coords_map_y(i, j) / rho(i, j));
        end
        %Drawing path
        for ii = 1:length(a)
            xp(i, j, ii) = R*cos(a(ii)+alpha0_sub)+rho(i, j)*cos(a(ii)*k + alpha0(i, j));
            yp(i, j, ii) = R*sin(a(ii)+alpha0_sub)+rho(i, j)*sin(a(ii)*k + alpha0(i, j));
            z(i, j, ii) =  F(xp(i, j, ii), yp(i, j, ii)); %get value z for xp, yp
            rel_th = 0;
        end
        for jj = 1:length(a)
            if jj > 1
                rel_th = rel_th + (z(i, j, jj-1) + z(i, j, jj))/2;
            else
                rel_th = rel_th + z(i, j, jj);
            end
        end
        I(i,j) = rel_th * deltat;
    end
end

%plot
%subplot(1,3,1)
figure(1)
surf(k_input, NR_input, I_var);
colormap(jet);
grid on
xlabel('k');
ylabel('NR');
title('Variance of spraing');

figure(2)
%subplot(1,3,2);
plot(substrate_coords_y,I(round(numel(substrate_coords_y)/2),:)./max(I(round(numel(substrate_coords_y)/2),:)), 'LineWidth', 2, 'Color', 'k', 'Marker', 'x')
grid on
xlabel('x, mm');
ylabel('y, rel unit');
title('Relative thickness along black line');

figure(3)
%subplot(1,3,3);
plot(substrate_coords_y,I(:,round(numel(substrate_coords_y)/2))./max(I(:,round(numel(substrate_coords_y)/2))), 'LineWidth', 2, 'Color', 'r', 'Marker', 'x')
grid on
xlabel('x, mm');
ylabel('y, rel unit');
title('Relative thickness along red line');