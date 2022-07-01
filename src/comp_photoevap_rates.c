//<FLAGS>
//#define __GPU
//#define __NOPROTO
//<\FLAGS>

//<INCLUDES>
#include "fargo3d.h"
//<\INCLUDES>

void ComputePhotoevapRates_cpu () {

//<USER_DEFINED>
  OUTPUT(SigmaDot);
//<\USER_DEFINED>

//<EXTERNAL>
  real* sdot = SigmaDot->field_cpu;
  int pitch  = Pitch_cpu;
  int stride = Stride_cpu;
  int size_x = Nx;
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

  real R0_in_m = 20*1.496E11;
  real Mstar_in_kg = 1.989E30;
  real g = 6.674E-11;
  real cs_in_m_per_s = 10E3;
  real time_unit_in_s = pow(R0_in_m, 1.5)/pow(g * Mstar_in_kg, 0.5);

  real C1 = 0.14;
  real A = 0.3423;
  real B = -0.3612;
  real D = 0.2457;

  real alpha = ((2.6E-13 * 1E-6) / (R0_in_m*R0_in_m*R0_in_m)) * time_unit_in_s; // 2.6e-13 cm^3/s in (R0)^3/(time unit)
  real cs = cs_in_m_per_s / R0_in_m * time_unit_in_s; // 10 km/s in R0/(time unit)
  real Rg = 1/(cs*cs); //  = GM/(cs)^2 = 1/(cs)^2 in code units

  real mu = 1.35; // mean molecular weight
  real mH = 1.67E-27 / Mstar_in_kg;  // mass of hydrogen, in units of Mstar

  real phi = PHI * time_unit_in_s; // photons/s => photons/(time unit)


  real ng = C1 * pow((3 * phi)/(4 * M_PI * alpha * Rg*Rg*Rg), 0.5);
  real R;
  real n0;
  real u1;
  real sigmaDotValue;

  i = j = k = 0;

#ifdef Z
  for (k=0; k<size_z; k++) {
#endif
#ifdef Y
    for (j=0; j<size_y; j++) {
      R = ymed(j);
      n0 = ng * pow(2 / (pow(R/Rg, 7.5) + pow(R/Rg, 12.5)), 0.2);
      u1 = cs * A * exp(B * ((R/Rg) - 0.1)) * pow((R/Rg) - 0.1, D);

      sigmaDotValue = 2*n0*u1*mu*mH;
#endif
#ifdef X
      for (i=0; i<size_x; i++ ) {
#endif
//<#>
	ll = l;
	sdot[ll] = sigmaDotValue;

  printf("ll=%d, j=%d, R=%.3e, SigmaDot=%.3e\n", ll, j, ymed(j), sigmaDotValue);
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
