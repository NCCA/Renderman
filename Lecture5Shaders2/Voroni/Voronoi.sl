#include "noises.h"
surface Voronoi
(
 float Ka=1;
 float roughness = 0.01;
 float Scale=0.1;
 float Layers=6;
 output float Freq=1;
 float RepeatX=0.5;
 float RepeatY=0.5;
 float RepeatZ=0.5;
)
{

/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

/* here we do the texturing */

point Ps= point(xcomp(P)/RepeatX,ycomp(P)/RepeatY,zcomp(P)/RepeatZ);
point PP = transform("shader",Ps);

point pos1;
float f1;
PP+=turbulence(Ps,0.2,2,1.8,3.0);

voronoi_f1_3d (PP, 0.8, f1, pos1);
color C1 = color(1,1,1);
color C2= color(0,0,0);
color Ct=mix(C1,C2,f1);
Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + 0.5*diffuse(Nf)) +specular(Nf,V,roughness));
}
