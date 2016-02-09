surface Check
(
 float Ka=1;
 float Kd=0.5;
 float Ks=0.5;
 float roughness = 0.1;
 color specularcolor = 1;
 color CheckColour = color "rgb" (0,0,0);
 float RepeatS=5;
 float RepeatT=5;
)
{
// init the shader values 
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

// here we do the texturing 
color Ct=Cs;
float sTile=floor(s*RepeatS);
float tTile=floor(t*RepeatT);
float inCheck=mod(sTile+tTile,2);
Ct=mix(Ct,CheckColour,inCheck);
// now calculate the shading values 

Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) 
		+ specularcolor * Ks  * specular(Nf,V,roughness));

}
