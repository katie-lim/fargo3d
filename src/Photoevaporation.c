//<FLAGS>
//#define __GPU
//#define __NOPROTO
//<\FLAGS>

//<INCLUDES>
#include "fargo3d.h"
//<\INCLUDES>

real sigmaDot[2000]; // an array to store the values of sigmaDot at each radius

// Units
const real R0_in_m = 20*1.496E11;
const real Mstar_in_kg = 1.989E30;
const real g = 6.674E-11;
const real cs_in_m_per_s = 15E3;

// Constants
const real C1 = 0.14;
const real A = 0.3423;
const real B = -0.3612;
const real D = 0.2457;


real calcng(real phi, real alpha, real Rg) {
  return C1 * pow((3 * phi)/(4 * M_PI * alpha * Rg*Rg*Rg), 0.5);
}

real calcn0(real R, real Rg, real phi, real alpha) {
  real ng = calcng(phi, alpha, Rg);

  return ng * pow(2 / (pow(R/Rg, 7.5) + pow(R/Rg, 12.5)), 0.2);
}

real calcVelocity(real R, real Rg, real cs) {
  return cs * A * exp(B * ((R/Rg) - 0.1)) * pow((R/Rg) - 0.1, D);
}

real calcSigmaDot(real R) {
  real time_unit_in_s = pow(R0_in_m, 1.5)/pow(g * Mstar_in_kg, 0.5);

  // Constants
  real alpha = ((2.6E-13 * 1E-6) / (R0_in_m*R0_in_m*R0_in_m)) * time_unit_in_s; // 2.6e-13 cm^3/s in (R0)^3/(time unit)
  real cs = cs_in_m_per_s / R0_in_m * time_unit_in_s; // 15 km/s in R0/(time unit)
  real Rg = 1/(cs*cs); //  = GM/(cs)^2 = 1/(cs)^2 in code units

  real mu = 1.35; // mean molecular weight
  real mH = 1.67E-27 / Mstar_in_kg;  // mass of hydrogen, in units of Mstar

  real phi = PHI * time_unit_in_s; // 4e43 photons/s in photons/(time unit)


  real n0 = calcn0(R, Rg, phi, alpha);
  real u1 = calcVelocity(R, Rg, cs);


  return 2*n0*u1*mu*mH;
}


void computePhotoevaporationRates() {
  // Computes and stores the value of sigmaDot at each radius

  int j = 0;
  int size_y = Ny+2*NGHY;

  printf("phi = %.3e photons/s \n", PHI);

  for (j=0; j<size_y; j++) {
    real R = ymed(j);

    sigmaDot[j] = calcSigmaDot(R);
    printf("R = %.3f, sigmaDot = %.3e \n", R, sigmaDot[j]);

  }
}

void Photoevaporation_cpu (real dt) {

//<USER_DEFINED>
  INPUT(Energy);
  INPUT(Density);
  OUTPUT(Pressure);
//<\USER_DEFINED>


//<EXTERNAL>
  real* dens = Density->field_cpu;
  real* cs   = Energy->field_cpu;
  real* pres = Pressure->field_cpu;
  int pitch  = Pitch_cpu;
  int stride = Stride_cpu;
  int size_x = Nx+2*NGHX;
  int size_y = Ny+2*NGHY;
  int size_z = Nz+2*NGHZ;
//<\EXTERNAL>

//<INTERNAL>
  int i;
  int j;
  int k;
  int ll;
//<\INTERNAL>

//<MAIN_LOOP>

  i = j = k = 0;

#ifdef Z
  for (k=0; k<size_z; k++) {
#endif
#ifdef Y
    for (j=0; j<size_y; j++) {
#endif
#ifdef X
      for (i=0; i<size_x; i++ ) {
#endif
//<#>

    ll = l;
    dens[ll] -= sigmaDot[j] * dt;


    real floor = 1E-15;
    if (dens[ll] < floor) {
      dens[ll] = floor;
    }


//<\#>
#ifdef X
      }
#endif
#ifdef Y
    }
#endif
#ifdef Z
  }
#endif

//<\MAIN_LOOP>
}
