
/*
 * Oren and Nayar's generalization of Lambert's reflection model.
 * The roughness parameter gives the standard deviation of angle
 * orientations of the presumed surface grooves.  When roughness=0,
 * the model is identical to Lambertian reflection.
 * Modified from the advanced renderman companion notes
 */
color
LocIllumOrenNayar (normal N;  vector V;  float roughness;)
{
    /* Surface roughness coefficients for Oren/Nayar's formula */
    float sigma2 = roughness * roughness;
    float A = 1 - 0.5 * sigma2 / (sigma2 + 0.33);
    float B = 0.45 * sigma2 / (sigma2 + 0.09);
    /* Useful precomputed quantities */
    float  theta_r = acos (V . N);        /* Angle between V and N */
    vector V_perp_N = normalize(V-N*(V.N)); /* Part of V perpendicular to N */

    /* Accumulate incoming radiance from lights in C */
    color  C = 0;
    extern point P;
    illuminance (P, N, PI/2) 
	{
	/* Must declare extern L & Cl because we're in a function */
		vector LN = normalize(L);
		float cos_theta_i = LN . N;
		float cos_phi_diff = V_perp_N . normalize(LN - N*cos_theta_i);
		float theta_i = acos (cos_theta_i);
		float alpha = max (theta_i, theta_r);
		float beta = min (theta_i, theta_r);
		C += Cl * cos_theta_i * 
		(A + B * max(0,cos_phi_diff) * sin(alpha) * tan(beta));
	}
    return C;
}





surface OrenNayar(float Ka=0.5;
				  float Kd=1.0;
				  float  roughness=0.2;
				  float Ks=0.5;
				  color specularcolor = 1;  

				)
{
/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

/* now calculate the shading values */

	
	
Oi=Os;
Ci= Oi *Cs * (Ka*ambient() + Kd*LocIllumOrenNayar(Nf,V,roughness)+specularcolor * Ks  * specular(Nf,V,roughness));
}