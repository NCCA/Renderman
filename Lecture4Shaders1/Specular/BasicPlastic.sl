surface BasicPlastic
(
 float Ka=1;
 float Kd=0.5;
 float Ks=0.5;
 float roughness = 0.1;
 color specularcolor = 1;
 string SpecType="phong";
 float size=0.05;
)
{
/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

/* now calculate the shading values */
color spec;
if( SpecType=="phong")	spec=specularcolor * Ks  * specular(Nf,V,size);else	spec=specularcolor * Ks  * specular(Nf,V,roughness);Oi=Os;
Ci= Oi * (Cs * (Ka * ambient() + Kd *diffuse(Nf)) +spec);

}
