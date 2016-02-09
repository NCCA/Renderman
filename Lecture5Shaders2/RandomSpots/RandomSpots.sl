surface RandomSpots
(
 float Ka=1;
 float Kd=0.5;
 float Ks=0.5;
 float roughness = 0.1;
 color specularcolor = 1;
 float RepeatS=5;
 float RepeatT=5;
 float fuzz=0.025;
)
{
// init the shader values 
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

// here we do the texturing 
color Ct=Cs;
point Center=point "world" (0.5,0.5,0);
float ss=mod(s*RepeatS,1);
float tt=mod(t*RepeatT,1);
point Here=point  "world" (ss,tt,0);	
float dist=distance(Center,Here);

float Radius = float cellnoise(RepeatS*s,RepeatT*t)*0.4;
color DiskColour=color cellnoise(RepeatS*s,RepeatT*t);	
float inDisk=1-smoothstep(Radius-fuzz,Radius+fuzz,dist);
Ct=mix(Cs,DiskColour,inDisk);
// now calculate the shading values 

Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) 
		+ specularcolor * Ks  * specular(Nf,V,roughness));

}
