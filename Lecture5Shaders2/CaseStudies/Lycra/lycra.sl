//**************************************************************//
//	Cloth Simulation - Shaders for Renderman
// 	Lycra Shader
//	Parameters: Color of cloth, color of sheen
//	Sheen changes with light, shows threads along Du direction
//*************************************************************//

#include "noises.h"
//#include "filterwidth.h"
//#include "patterns.h"


surface lycra(	float Ka= 0.5;
				float Ks = 0.01;
				float Kd = 1;
				float Kr = 0.05;
				float roughness = 5;
    			float specularcolor = 0.01;
				float fuzz = 0.010;
				string bumpTex="denim.tx";
				uniform float octaves  = 6;
				uniform float lacunarity = 1;
				uniform float gain = 0.05;
				float RepeatS=4.0;
				float RepeatT=4.0;
			)

{
//**************************************************//
//			Colours Used							//
//**************************************************//
color white = color "rgb" (1,1,1);
color black = color "rgb" (0,0,0);
color blue = color "rgb" (0,0,1);
color red = color "rgb" (1,0,0);
color green = color "rgb" (0,1,0);
color grey = color "rgb" (0.4, 0.4, 0.4);

color green1 = color "rgb" (0,0.648,0.438);
color blue1 = color "rgb" (0.219, 0.243, 0.648);
color red1 = color "rgb" (0.648, 0.105, 0.133);
color pink1 = color "rgb" (1, 0.804, 0.745);

color navy = color "rgb" (0.2, 0.2, 0.45);
color navy2 = color "rgb" (0.15, 0.15, 0.5);

color denim1 = color "rgb" (0.286, 0.400, 0.525);
color denim2 = color "rgb" (0.627, 0.741, 0.906);
color denim3 = color "rgb" (0.196, 0.275, 0.369);
color GoldStitch = color "rgb" (0.941, 0.749, 0.251);
color Silver = color "rgb" (0.917, 0.917, 0.908);
color Gold = color "rgb" (0.933, 0.843, 0.443);


color green2 = color "rgb" (0.022 ,0.395,0.078);
color blue2 = color "rgb" (0.162, 0.140, 0.395);
color red2 = color "rgb" (0.533, 0.153, 0.133);
color pink2 = color "rgb" (0.533, 0.055, 0.431);

//**************************************************//
//	Point and normal info							//
//**************************************************//

point PP = transform("shader", P);

normal Nf = faceforward (normalize(N), I);
vector V = -normalize(I);

float xroughness = 0.5;
float yroughness = 0.5;
vector xDir = normalize(dPdu);
vector aDir = normalize( (Dv(P) + 2 *Du(P) )/3);
vector Dir = normalize( Du(P) );

vector X = xDir / xroughness;
vector Y = (N * xDir) / yroughness;
color Ct;
color anisotrop;


color stitch1 = 0;
color stitch2 = 0;
color stitch3 = 0;
color DenimShadow = 0;

float freq1 = 500;
float freq2 = 100;

color threads;
float ss=mod(s*RepeatS,1);
float tt=mod(t*RepeatT,1);

threads = mix(blue1, white, fBm(PP, filterwidthp(PP), octaves, lacunarity, gain));
stitch1 = mix(white, black, pnoise(tt/ss*freq1, 0.5) );
stitch2 = mix(black, white, pnoise(ss/tt*freq2, 1) );


float Jeans = texture(bumpTex, ss, tt);


//**********************************//
// Bump map stuff					//
//**********************************//
//use the jeans texture as a bump map
normal NN = normalize(N);

float thread = (ss * freq1)* Jeans;
PP = P + NN * thread;

N = calculatenormal(PP);

normal Nff = faceforward (normalize(N), I);



//use illuminance loop to make threads a different
//color based on the light on them
illuminance(P, Nf, PI/2)
	{
	color MyCl;

	float MyCos;
	float MySin;

	//vector Ln = normalize(L);
	vector Vn = normalize(V);

	//this helps to give it a lycra feel
	//mix between the Fabric colour and the underneath sheen based on the angle from the normal and the vector v
	MyCos = max ( Nff.Vn, 0 );
	DenimShadow += mix(GoldStitch, Silver, smoothstep(0.2, 0.8, MyCos) );
	 }


Ct = stitch1 * stitch2 + 0.3 * DenimShadow;


//for matte shading
Ci = Oi * Ct * (Ka*ambient() + Kd * diffuse(Nf));
}

