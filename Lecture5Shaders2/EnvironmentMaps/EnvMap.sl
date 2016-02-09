float sqr (float x) { return x*x; }color LocIllumWardAnisotropic (normal N;  vector V;                         vector xdir;  float xroughness; float yroughness;						){    float cos_theta_r = clamp (N.V, 0.0001, 1);    vector X = xdir / xroughness;    vector Y = (N ^ xdir) / yroughness;    color C = 0;    illuminance (P, N, PI/2) 	{	    vector LN = normalize (L);	    float cos_theta_i = LN . N;	    if (cos_theta_i > 0.0) 			{			vector H = normalize (V + LN);			float rho = exp (-2 * (sqr(X.H) + sqr(Y.H)) / (1 + H.N))		    / sqrt (cos_theta_i * cos_theta_r);			C += Cl * (  cos_theta_i * rho);			}    }    return C / (4 * xroughness * yroughness);}



surface EnvMap
(
 float Ka=1; float Kd=.5;
 float Ks=.4; float Kr=.3;
 float roughness = 0.1;
 color specular=1;
 string MapName="";
float xroughness=0.5;float yroughness=0.5;
)
{

// init the shader values 
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

// here we do the texturing 

color spec = LocIllumWardAnisotropic (Nf, V, normalize(dPdu), xroughness, yroughness);
color Ct;
vector Rcurrent=reflect(I,Nf);
vector Rworld=vtransform("world",Rcurrent);
color Cr=color environment(MapName,Rworld);
// now calculate the shading values 
Ct=Cs;
Oi=Os;
Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) + 
	specular * (Ks*spec+Kr*Cr));


}
