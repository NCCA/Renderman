//**************************************************//
//	Cloth Simulation - Shaders for Renderman
// 	Tartan Shader
// Original Shader by Elaine Kieran  MSc CA 05
// Modified by Jon Macey
//**************************************************//

#include "material.h"

surface tartan(	float Ka= 1;
				float Ks = 0.1;
				float Kd = 1;
				float roughness = 1;
    			float specularcolor = 0.1;
				float fuzz = 0.010;
				color ClothBack = color "rgb" (0.4, 0.4, 0.4);
				color Fleece1Colour = color "rgb" (0.533, 0.153, 0.133);
				color Fleece2Colour = color "rgb" (0.162, 0.140, 0.395);
				color Fleece3Colour = color "rgb" (0.022 ,0.395,0.078);
				color Fleece3BGColour = color "rgb" (0,0,0);
				color Fleece4Colour = color "rgb" (0,0,0);
				color Fleece4BGColour = color "rgb" (0.162, 0.140, 0.395);
				float freq1 = 10;
				float freq2 = 10;
				float RepeatS=1;
				float RepeatT=1;
			  )

{
//**************************************************//
//	Point and normal info							//
//**************************************************//

point PP = transform("shader", P);
normal Nf = faceforward (normalize(N), I);
vector V = -normalize(I);

color Ct;

color fleece1 = 0;
color fleece2 = 0;
color fleece3 = 0;
color fleece4 = 0;



// create different colour layers
fleece1 = mix(Fleece1Colour, ClothBack, pnoise( RepeatT*t*freq1, 3) );
fleece2 = mix(Fleece2Colour, ClothBack,pnoise(RepeatS* s*freq2, 5) );

fleece3 = mix( Fleece3Colour, Fleece3BGColour, cellnoise( RepeatS*s*5, fuzz) );
fleece4 = mix( Fleece4Colour, Fleece4BGColour, cellnoise( RepeatT*t*5, fuzz) );
// combine them
Ct = fleece3 + fleece1 + fleece2 + fleece4;


// use Oren Nayer Clay material from ARMAN notes
Ci = Oi * MaterialClay(Nf,Ct,Ka,Kd,roughness);
}

