M = [2 0; 0 1];
K = [6 -2; -2 4];

[V,D] = eig(K,M);

omega = sqrt(diag(D));

disp('Eigenvalues (omega^2):')
disp(diag(D))

disp('Natural frequencies (rad/s):')
disp(omega)

disp('Mode shapes:')
disp(V)