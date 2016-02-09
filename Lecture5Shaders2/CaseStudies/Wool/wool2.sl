//**************************************************//
//	Cloth Simulation - Shaders for Renderman
// 	Denim Shader
//	Parameters:
//**************************************************//





surface wool2(	float Ka= 0.5;
				float Ks = 0.01;
				float Kd = 1;
				float Kr = 0.1;
				float fuzz = 0.010;
				float RepeatS=4.0;
				float RepeatT=4.0;
				uniform float octaves  = 6;
				uniform float lacunarity = 1;
				uniform float gain = 0.05;
				
			)

{
//**************************************************//
//			Colours Used							//
//**************************************************//

color white = color "rgb" (1,1,1);
color blue = color "rgb" (0,0,1);
color grey = color "rgb" (0.4, 0.4, 0.4);
color blue1 = color "rgb" (0.219, 0.243, 0.648);
color blue2 = color "rgb" (0.162, 0.140, 0.395);
color navy = color "rgb" (0.2, 0.2, 0.45);
color navy2 = color "rgb" (0.15, 0.15, 0.5);
color denim1 = color "rgb" (0.286, 0.400, 0.525);
color denim2 = color "rgb" (0.627, 0.741, 0.906);
color denim3 = color "rgb" (0.196, 0.275, 0.369);
color GoldStitch = color "rgb" (0.941, 0.749, 0.251);

//**************************************************//
//	Point and normal info							//
//**************************************************//

point PP = transform("shader", P);
normal Nf = faceforward (normalize(N), I);
vector V = -normalize(I);

color Ct;
color stitch1 = 0;
color stitch2 = 0;
color stitch3 = 0;

float freq1 = 500;
float freq2 = 100;
float ss=mod(s*RepeatS,1);
float tt=mod(t*RepeatT,1);
string JeansTex = "testfib2.tx";
float Jeans = texture(JeansTex, ss, tt);


//*********************************
// Bump Mapping Code
//*********************************

normal NN = normalize(N);

float thread = (ss * freq1)* Jeans;
PP = P + NN * thread;
N = calculatenormal(PP);
normal Nff = faceforward (normalize(N), I);

stitch1 = mix(white, navy, pnoise(tt/ss*freq1, 150) );
stitch2 = mix(denim2, white, pnoise(ss/tt*freq1, 100) );


Ct = stitch1 * stitch2 + 0.3 * Jeans;

Ci = Oi * Ct * (Ka*ambient() + Kd * diffuse(Nf));
}

