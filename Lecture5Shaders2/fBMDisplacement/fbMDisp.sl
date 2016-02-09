displacement fbmDisp
(
 float Km=0.1;
 float Layers=6;
 output varying float Freq=1;
)
{

/* init the shader values */
vector NN=normalize(N);
float i;
float mag=0;
point Pt=transform("shader",P);
for(i=0; i<Layers; i+=1)
	{
	mag+=(float noise(Pt*Freq)-0.5)*2/Freq;
	Freq*=2;
	}
mag /=length(vtransform("object",NN));
P=P+mag*NN*Km;
N=calculatenormal(P);

}
