//***************************************************************//
//	Cloth Simulation - Shaders for Renderman
// 	Velvet Shader
//	Parameters: Color of cloth
//	Adapted from Velvet shader by Stephen H. Westin,
//  http://www.renderman.org/RMR/Shaders/SHWShaders/SHW_velvet.sl
//***************************************************************//

surface velvet(	float Ka= 1;
				float Ks = 0.01;
				float Kd = 0.3;
				float Kr = 0.5;
				float roughness = 0.05;
    			float specularcolor = 0.1;
				float fuzz = 0.010;
				color SheenColour= color "rgb" (0,0.648,0.438);
				uniform float octaves  = 6;
				uniform float lacunarity = 2;
				uniform float gain = 0.5;
			  )

{
//**************************************************//
//	Point and normal info							//
//**************************************************//

point PP = transform("shader", P);

float tt = t;
float ss = s;

normal Nf = faceforward (normalize(N), I);
vector V = -normalize(I);

float xroughness = 0.5;
float yroughness = 0.5;
vector xDir = normalize(dPdu);
vector aDir = normalize( (Dv(P) + 2 *Du(P) )/3);

vector Dir = normalize( Du(P) );
vector Dirv = normalize (Dv(P) );

float freq = 2;
float depth = 2;

//the direction of the threads is alternated
vector MyDir= Dir / 0.5 ;

vector MyDir1 = Dir *random();
vector MyDir2 =aDir;

float d = noise(freq*s) + noise(freq*t) - 1; // from -1 to 1
vector MyDird = N *depth *d;


vector X = xDir / xroughness;
vector Y = (N * xDir) / yroughness;
color Ct;
color Caniso = 0;

float mag = 0;
float magt = 0;


color Velvet = 0;

illuminance(P, Nf, PI/2)
	{
	color MyCl = VelvetColour;

	float MyCos;
	float MySin;

	float reflect = 0.3;
	float highlight = 0.5;
	float strength = 8;

	vector Ln = normalize(L);
	vector Vn = normalize(V);

	MyCos = max(Dir.Vn, 0);

    Velvet += pow ( MyCos, 1.0/roughness ) * reflect *  Cl * highlight;

    MyCos = max ( Nf.Vn, 0 );
    MySin = sqrt (1.0-(MyCos * MyCos));

    Velvet += pow ( MySin, strength ) *  Cl * highlight *MyCl;
	 }


Oi = Os;

Ci = Oi *  ( Velvet + Cs *(ambient() + Kd * diffuse(Nf)));

}

