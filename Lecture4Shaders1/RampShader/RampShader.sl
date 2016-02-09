surface RampShader(
 color BlendColor = color "rgb" (0,1,0);
 float orientation = 0; 
 float Ka=1;
 float Kd=0.5;
 float Ks=0.5;
 float roughness = 0.1;
 color specularcolor = 1;
)
{
// init the shader values 
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);


color Ct;

// here we do the texturing 
if(orientation ==0)
        Ct=mix(Cs,BlendColor,s);
else
        Ct=mix(Cs,BlendColor,t);
// now calculate the shading values 
Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) + specularcolor * Ks  * specular(Nf,V,roughness));
}