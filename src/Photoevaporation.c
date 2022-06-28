//<FLAGS>
//#define __GPU
//#define __NOPROTO
//<\FLAGS>

//<INCLUDES>
#include "fargo3d.h"
//<\INCLUDES>

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
  real* sigmaDotInternalPtr = sigmaDot_cpu;
//<\EXTERNAL>

//<INTERNAL>
  int i;
  int j;
  int k;
  int ll;
  real floor = 1E-15;
//<\INTERNAL>

//<CONSTANT>
// real ymin(Ny+2*NGHY+1);
// real zmin(Nz+2*NGHZ+1);
//<CONSTANT>

//<MAIN_LOOP>

  i = j = k = 0;

#ifdef Z
  for (k=0; k<size_z; k++) {
#endif
#ifdef Y
    for (j=0; j<size_y; j++) {
    // Debugging
    printf("j = %d, R = %.3e, sigmaDot = %.3e", j, ymed(j), sigmaDotInternalPtr[j])
#endif
#ifdef X
      for (i=0; i<size_x; i++ ) {
#endif
//<#>

    ll = l;
    dens[ll] -= sigmaDotInternalPtr[j] * dt;

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
