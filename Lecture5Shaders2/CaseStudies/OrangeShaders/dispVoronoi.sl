#include "noises.h"

displacement dispVoronoi
(
 
 float roughness = 0.01;
 float Scale=0.1;
 
 float Freq=1;
 float RepeatX=0.03;
 float RepeatY=0.05;
 float RepeatZ=0.05;
 float Km = 0.002
)
{
	uniform float frequency = 5, maxoctaves = 9; 
	string shadingspace = "shader";
      
		
	point Pshad = transform (shadingspace, frequency*P);
    float dPshad = filterwidthp(Pshad);
    float magnitude = fBm (Pshad, dPshad, maxoctaves, 2, 0.5);
	
	


/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

/* here we do the texturing */

point Ps= point(xcomp(P)/RepeatX,ycomp(P)/RepeatY,zcomp(P)/RepeatZ);
point PP = transform("shader",Ps);

point pos1;
float f1;
voronoi_f1_3d (PP, 0.8, f1, pos1);

P += Km * magnitude * normalize(N);
  N = calculatenormal(P);
}
