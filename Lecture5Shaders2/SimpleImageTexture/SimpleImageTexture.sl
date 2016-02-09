surface SimpleTexture
(
 float Ka=1;float Kd=0.5;
 float Ks=0.5; float roughness = 0.1;
 color specularcolor = 1;
 string TextureName="";
 float RepeatS=1; float RepeatT=1;
)

{

// init the shader values 

normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

// here we do the texturing 

color Ct=Cs;
	
float ss=mod(s*RepeatS,1.0);
float tt=mod(t*RepeatT,1.0);
// set Ct to be the base colour if we have a texture file
// then change the value
Ct=Cs;	
if(TextureName !="")
        Ct=texture(TextureName,ss,tt);
/* now calculate the shading values */
Oi=Os;

Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) + 
		specularcolor * Ks  * specular(Nf,V,roughness));
}