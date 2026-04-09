% Demonstration: random numbers fall on planes (xorshift128+)
% Based on Haramoto & Matsumoto (2019), ACM Trans. Math. Softw.
%
% The paper shows that consecutive triple outputs (x, y, z) of the
% xorshift128+ generator tend to cluster on a small set of planes
% in 3D space, violating the expected uniform distribution.
%
% Generator parameters (a, b, c).
% NOTE: The paper uses a=23 for its figures (Figures 4 and 5).
%       Using a=5 here reduces the filtering step and speeds up
%       rendering, but the structural defect is still visible.
a = 5;
b = 17;
c = 26;

% --- Internal 128-bit state: two 64-bit unsigned integers ---
% Input:  arbitrary nonzero seed pair
% Output: these values are mutated on every call to the recurrence
s0 = uint64(123456789);
s1 = uint64(987654321);

num_points   = 5000;
x_values     = zeros(num_points, 1);   % filtered x outputs, normalized to [0, 1)
y_values     = zeros(num_points, 1);   % corresponding y outputs
z_values     = zeros(num_points, 1);   % corresponding z outputs
counter      = 1;

% 2^64 as a double for normalization. Note: double has 53-bit mantissa,
% so the lower bits of a uint64 are lost, but the MSBs used by the
% paper's analysis are preserved correctly.
divisor      = 2^64;

% x_threshold replicates the paper's filter condition: x <= 1/2^a
% (Section 3, Figure 4). Only triples where x falls in this narrow
% band are collected, because the planar structure is clearest there.
x_threshold  = 1 / (2^a);

disp('Generating states and filtering for hyperplane structure...');

while counter <= num_points

    % Collect three consecutive outputs (x, y, z) as defined in
    % Section 3 of the paper:
    %   x = s_i   + s_{i+1} mod 2^64
    %   y = s_{i+1} + s_{i+2} mod 2^64
    %   z = s_{i+2} + s_{i+3} mod 2^64
    outputs = zeros(3, 1);

    for i = 1:3
        % --- xorshift128+ recurrence (Equation 1 of the paper) ---
        % State before this step: (s0, s1) = (s_i, s_{i+1})
        %
        % Step 1: advance the state window.
        %   new s0 <- old s1   (i.e., s_{i+1} becomes the first word)
        old_s0 = s0;
        old_s1 = s1;
        s0     = old_s1;

        % Step 2: compute s_{i+2} per Equation 1:
        %   s_{i+2} = s_i * (I xor L^a) * (I xor R^b)
        %             xor s_{i+1} * (I xor R^c)
        %
        %   t = old_s0 xor (old_s0 << a)         [applies (I xor L^a)]
        t  = bitxor(old_s0, bitshift(old_s0, a));

        %   new s1 = (t xor (t >> b))             [applies (I xor R^b) to t]
        %            xor (old_s1 xor (old_s1 >> c)) [applies (I xor R^c)]
        s1 = bitxor(t, bitxor(old_s1, ...
                    bitxor(bitshift(t, -b), bitshift(old_s1, -c))));
        % State after this step: (s0, s1) = (s_{i+1}, s_{i+2})

        % --- Output function (Section 1 of the paper) ---
        % o_i = s_i + s_{i+1} mod 2^64
        % After the state advance above, s0 = s_{i+1}, s1 = s_{i+2},
        % so this computes s_{i+1} + s_{i+2}, which is the next output.
        % uint64 addition in MATLAB wraps automatically mod 2^64.
        %
        % Input:  s0, s1 (uint64)
        % Output: raw_output normalized to the interval [0, 1)
        raw_output   = s0 + s1;
        outputs(i)   = double(raw_output) / divisor;
    end

    x = outputs(1);
    y = outputs(2);
    z = outputs(3);

    % --- Filter: keep only triples where x <= 1/2^a ---
    % This replicates the paper's method for Figure 4:
    % "We only pick up those with x <= 1/2^23, and plot (2^23 * x, y, z)."
    % The filter isolates a thin slab of the cube where the planar
    % structure is unambiguous.
    if x <= x_threshold
        x_values(counter) = x;
        y_values(counter) = y;
        z_values(counter) = z;
        counter = counter + 1;
    end
end

% --- X-axis magnification (Section 3, Figure 4) ---
% Scaling x by 2^a stretches the thin slab [0, 1/2^a] back to [0, 1],
% making the planar clusters visible at the scale of the full unit cube.
% Input:  x_values in [0, 1/2^a)
% Output: x_scaled in [0, 1)
x_scaled = x_values * (2^a);

% --- Visualization ---
figure('Name', 'xorshift128+ Planes', 'Position', [100, 100, 800, 600]);
scatter3(x_scaled, y_values, z_values, 10, 'filled', ...
         'MarkerFaceColor', 'k', 'MarkerFaceAlpha', 0.6);

title(sprintf('xorshift128+ structural failure (a=%d)\nX-axis magnified by 2^{%d}', a, a), ...
      'FontSize', 12);
xlabel('x (magnified)', 'FontWeight', 'bold');
ylabel('y',             'FontWeight', 'bold');
zlabel('z',             'FontWeight', 'bold');

% Unit cube bounds match the paper (Figures 4 and 5).
xlim([0 1]); ylim([0 1]); zlim([0 1]);
grid on;
view(-45, 20);   % Viewing angle chosen to expose the planar slices

disp('Plot ready. Rotate the cube to observe the planar concentration described in the paper.');