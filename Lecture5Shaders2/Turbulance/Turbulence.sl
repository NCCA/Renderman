surface Turbulence
(
 float Ka=1;
 float Kd=1;
 float roughness = 0.01;
 float Scale=0.1;
 float Layers=4;
 output varying float StartFreq=4;
 float gain=4;
 float lacunarity=1.9132;
 string noiseSpace="shader";
)
{

/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

/* here we do the texturing */
float i;
float mag=0;
float freq=1;
point PP=transform(noiseSpace,P);
PP*=StartFreq;

for(i=0; i<Layers; i+=1)
	{
	mag+=abs(float noise(PP*freq)-0.5)*2/pow(freq,gain);
	freq*=lacunarity;
	}
/* now calculate the shading values */
color Ct=mag;
Oi=Os;
Ci = Os * (Ct * ( Ka*ambient() + Kd*diffuse(Nf) ) );

}
