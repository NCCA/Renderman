surface Layer
(
 float Ka=1;
 float Kd=1;
 float Scale=0.1;
 float Layers=6;
 output varying float Freq=1;
)
{

/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

/* here we do the texturing */
float i;
float mag=0;
point Pt=transform("shader",P);
for(i=0; i<Layers; i+=1)
	{
	mag+=(float noise(Pt*Freq)-0.5)*2/Freq;
	Freq*=2;
	
	
	}
/* now calculate the shading values */
color Ct=mag+0.5;
Oi=Os;
Oi = Os;Ci = Os * (Ct * ( Ka*ambient() + Kd*diffuse(Nf) ) );
}
