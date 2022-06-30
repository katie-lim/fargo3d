//<INCLUDES>
#include "fargo3d.h"
//<\INCLUDES>

real CalcSigmaDot_cpu(real R) {
    // Units
    const real R0_in_m = 20*1.496E11;
    const real Mstar_in_kg = 1.989E30;
    const real g = 6.674E-11;
    const real cs_in_m_per_s = 10E3;
    const real time_unit_in_s = pow(R0_in_m, 1.5)/pow(g * Mstar_in_kg, 0.5);

    // Constants
    const real C1 = 0.14;
    const real A = 0.3423;
    const real B = -0.3612;
    const real D = 0.2457;

    real alpha = ((2.6E-13 * 1E-6) / (R0_in_m*R0_in_m*R0_in_m)) * time_unit_in_s; // 2.6e-13 cm^3/s in (R0)^3/(time unit)
    real cs = cs_in_m_per_s / R0_in_m * time_unit_in_s; // 10 km/s in R0/(time unit)
    real Rg = 1/(cs*cs); //  = GM/(cs)^2 = 1/(cs)^2 in code units

    real mu = 1.35; // mean molecular weight
    real mH = 1.67E-27 / Mstar_in_kg;  // mass of hydrogen, in units of Mstar

    real phi = PHI * time_unit_in_s; // photons/s => photons/(time unit)


    real ng = C1 * pow((3 * phi)/(4 * M_PI * alpha * Rg*Rg*Rg), 0.5);
    real n0 = ng * pow(2 / (pow(R/Rg, 7.5) + pow(R/Rg, 12.5)), 0.2);
    real u1 = cs * A * exp(B * ((R/Rg) - 0.1)) * pow((R/Rg) - 0.1, D);


    return 2*n0*u1*mu*mH;
}


void ComputePhotoevaporationRates_cpu() {
    // Computes and stores the value of sigmaDot at each radius
    printf("Phi = %.3e photons/s \n", PHI);

    int size_y = Ny+2*NGHY;
    sigmaDot_cpu = (real *) malloc(sizeof(real) * size_y);

#IFDEF GPU
    DevMalloc(&sigmaDot_gpu,sizeof(real)*(Ny+2*NGHY));
#ENDIF

    int j = 0;
    for (j=0; j<size_y; j++) {
        real R = ymed(j);

        sigmaDot_cpu[j] = CalcSigmaDot_cpu(R);
        printf("R = %.3f, sigmaDot = %.3e \n", R, sigmaDot_cpu[j]);

    }
}