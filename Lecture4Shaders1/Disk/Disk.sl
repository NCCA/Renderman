surface Disk
(
 float Ka=1;
 float Kd=0.5;
 float Ks=0.5;
 float roughness = 0.1;
 color specularcolor = 1;
 color DiskColour = color "rgb" (1,1,1);
 point center = point "shader" (0.5,0.5,0.0);
 float fuzz=0.025;
 float Radius = 0.5;
 float RepeatS=5;
 float RepeatT=5;
)
{
/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

/* here we do the texturing */
color Ct=Cs;
float ss=mod(s*RepeatS,1);
float tt=mod(t*RepeatT,1);
	
point here = point "shader" (ss,tt,0);
float dist=distance(center,here);
float inDisk=1-smoothstep(Radius/2.0-fuzz,Radius/2.0+fuzz,dist);
Ct=mix(Ct,DiskColour,inDisk);
/* now calculate the shading values */

Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) 
		+ specularcolor * Ks  * specular(Nf,V,roughness));

}
