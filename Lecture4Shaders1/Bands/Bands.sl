surface Band(
 color C1 = color "rgb" (1,0,0);
 color C2 = color "rgb" (0,0,1);
 float begin=0.3;
 float end=0.6;
 float Ka=1;
 float Kd=0.5;
 float Ks=0.5;
 float roughness = 0.1;
 color specularcolor = 1;
 float Orient=0;
)
{
// init the shader values 
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);


color Ct;

// here we do the texturing 

float inTop;
if (Orient==0)
	inTop = smoothstep(begin,end,s);
else
	inTop = smoothstep(begin,end,t);
	
Ct=mix(C1,C2,inTop);	
// now calculate the shading values 
Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) + specularcolor * Ks  * specular(Nf,V,roughness));
}
