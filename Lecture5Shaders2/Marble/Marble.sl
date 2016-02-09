
surface Marble
(
 float Ka=1; float Kd=0.5; float Ks=0.5;
 float roughness = 0.01;
 float Scale=0.76;
 float Layers=21;
 output varying float StartFreq=2;
 float gain=0.86;
 float lacunarity=1.74;
 float Repeat=1.0;
 string noiseSpace="shader";
 color specularcolor=1;
 float ColourLayers=4;
 color Colour1= color "rgb" (0.051 ,0.059, 0.596);
 color Colour2= color "rgb" (0.365 ,0.369, 0.635);
 color Colour3= color "rgb" (1.000 ,0.976, 0.988);
 float rDiff=0.05;
 float gDiff=0.05;
 float bDiff=0.05;
)
{

/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

/* here we do the texturing */
float i;
float mag=0;
float freq=StartFreq;
point PP=transform(noiseSpace,P);
PP*=Scale;

for(i=0; i<Layers; i+=1)
	{
	mag+=abs(float noise(P*Repeat*freq)-0.5)*2/freq;
	freq*=lacunarity;	
	}
/* now calculate the shading values */
mag=smoothstep(0,0.4,mag);
color MColours[];
push(MColours,Colour1);
float rC=rDiff;	
float gC=gDiff;
float bC=bDiff;
// build up an array of colours for the spline function
color Ca;
push(MColours,Colour1);

Ca=color "rgb"(Colour1[0]-rC,Colour1[1]-gC,Colour1[2]-bC);
for (i=0; i<ColourLayers; i+=1)
	{
	push(MColours,Ca);
	Ca=color "rgb"(Ca[0]-rC,Ca[1]-gC,Ca[2]-bC);
	}
push(MColours,Colour2);
	
Ca=color "rgb"(Colour2[0]-rDiff,Colour2[1]-gDiff,Colour2[2]-bDiff);
for (i=0; i<ColourLayers; i+=1)
	{
	push(MColours,Ca);
	Ca=color "rgb"(Ca[0]-rC,Ca[1]-gC,Ca[2]-bC);
	}
push(MColours,Colour3);
	
Ca=color "rgb"(Colour3[0]-rDiff,Colour3[1]-gDiff,Colour3[2]-bDiff);
for (i=0; i<ColourLayers; i+=1)
	{
	push(MColours,Ca);
	Ca=color "rgb"(Ca[0]-rC,Ca[1]-gC,Ca[2]-bC);
	}
	
// now select the colour from the spline function	
color Ct=spline(mag,MColours);
Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + Kd*diffuse(Nf)) +specularcolor *Ks *specular(Nf,V,roughness));

}
