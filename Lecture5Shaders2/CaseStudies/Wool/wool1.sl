//**************************************************************//
//	Cloth Simulation - Shaders for Renderman
// 	Wool Shader
//	Parameters:
//	Stripe 1 - color of first stripe along t
//	Stripe 2 - color of second stripe along t
//
//	Stripe 1 - color of first stripe along s
//	Stripe 2 - color of second stripe along s
//
//	Texture map for fibres
//*************************************************************//

//#include "noises.h"
//#include "filterwidth.h"
//#include "patterns.h"


surface wool(	float Ka= 1;
				float Ks = 0.1;
				float Kd = 1;
				float Kr = 0.5;
				float roughness = 1;
    			float specularcolor = 0.1;
				float fuzz = 0.010;

				uniform float octaves  = 6;
				uniform float lacunarity = 1;
				uniform float gain = 0.05;
				float RepeatS=4.0;
				float RepeatT=4.0;
				color Stripe1 = color "rgb" (0.648, 0.105, 0.133);
				color Stripe2 = color "rgb" (1, 0.804, 0.745);
				color Stripe3 = color "rgb" (0,0.648,0.438);
				color Stripe4 = color "rgb" (0.219, 0.243, 0.648);

			)

{



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


//**************************//
// Color Variables			//
//**************************//
color stitch = 0;
color stitch2 = 0;
color fleece1;
color fleece2;

float freq1 = 10;
float freq2 = 10;


//******************************//
// Texture map for wool fibres	//
//******************************//
float ss=mod(s*RepeatS,1);
float tt=mod(t*RepeatT,1);
string WoolTex = "wool.tx";
color wool = texture(WoolTex, ss, tt);


//**************************************//
// mix to get check / tartan effect
// Uses colours passed in
//**************************************//
fleece1 = mix(Stripe1, Stripe2, noise(tt*freq1) );
fleece2 = mix(Stripe3, Stripe4, noise(ss*freq2) );


//****************************************//
//add the texture to the tartan pattern
//****************************************//
Ct = wool * (fleece1 + fleece2);


//for rough metal
Ci = Oi * Ct * (Ka*ambient() + Kd * diffuse(Nf) + Ks*specular(Nf, V, roughness));
}

