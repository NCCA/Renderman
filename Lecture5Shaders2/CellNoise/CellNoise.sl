surface CellNoise
(
 float Ka=1;
 float Kd=0.5;
 float Ks=0.5;
 float roughness = 0.1;
 color specularcolor = 1;
 float RepeatS=5;
 float RepeatT=5;
)
{
// init the shader values 
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

// here we do the texturing 
color Ct=Cs;
float ss=s*RepeatS;
float tt=t*RepeatT;
Ct=color cellnoise(ss,tt);
// now calculate the shading values 

Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) 
		+ specularcolor * Ks  * specular(Nf,V,roughness));

}
