surface UserLines
(
 color LineColor = color "rgb" (1,0,0);
 float LineSize=0.01;
 float Ka=1;
 float Kd=0.5;
 float Ks=0.5;
 float roughness = 0.5;
 color specularcolor = 1;
 point P1= point "shader" (0.1,0.7,0);
 point P2= point "shader" (0.7,0.7,0);
 float fuzz = 0.025;
)
{
/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

/* here we do the texturing */
color Ct=Cs;
// we need this point in shader space so it is on the surface of the
// object we are shading
point Here = point "shader" (s,t,0);
float dist=ptlined(P1,P2,Here);
float inLine = 1-smoothstep(LineSize/2.0-fuzz,LineSize/2.0+fuzz,dist);
Ct=mix(Ct,LineColor,inLine);

Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) 
		+ specularcolor * Ks *specular(Nf,V,roughness)  );

}
