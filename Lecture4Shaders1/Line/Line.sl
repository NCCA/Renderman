surface Lines
(
 color LineColor = color "rgb" (1,0,0);
 color MixColor = color "rgb" (1,1,1);
 float fuzz = 0.025;
 float LineSize=0.1;
 float Ka=1;
 float Kd=0.5;
 float Ks=0.5;
 float roughness = 0.1;
 color specularcolor = 1;
 float Orient=0;
 float offset=0.5;
)
{
/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);
color Ct;

/* here we do the texturing */
float inTop;
float dist;
if(Orient==0)
	dist=abs(t-offset);
else 
	dist=abs(s-offset);
float inLine;

inTop=1-smoothstep(LineSize/2.0-fuzz,LineSize/2.0+fuzz,dist);
Ct=mix(MixColor,LineColor,inTop);


/* now calculate the shading values */

Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) + specularcolor * Ks  * specular(Nf,V,roughness));

}
