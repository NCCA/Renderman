/*
 * Greg Ward Larson's anisotropic specular local illumination model.
 * The derivation and formulae can be found in:  Ward, Gregory J.
 * "Measuring and Modeling Anisotropic Reflection," ACM Computer 
 * Graphics 26(2) (Proceedings of Siggraph '92), pp. 265-272, July, 1992.
 * Notice that compared to the paper, the implementation below appears
 * to be missing a factor of 1/pi, and to have an extra L.N term.
 * This is not an error!  It is because the paper's formula is for the
 * BRDF, which is only part of the kernel of the light integral, whereas
 * shaders must compute the result of the integral.
 *
 * Inputs:
 *   N - unit surface normal
 *   V - unit viewing direction (from P toward the camera)
 *   xdir - a unit tangent of the surface defining the reference
 *          direction for the anisotropy.
 *   xroughness - the apparent roughness of the surface in xdir.
 *   yroughness - the roughness for the direction of the surface 
 *          tangent perpendicular to xdir.
 */
float sqr (float x) { return x*x; }

color LocIllumWardAnisotropic (normal N;  vector V;
                         vector xdir;  float xroughness; float yroughness;
						)
{

    float cos_theta_r = clamp (N.V, 0.0001, 1);
    vector X = xdir / xroughness;
    vector Y = (N ^ xdir) / yroughness;

    color C = 0;
    illuminance (P, N, PI/2) 
	{
	    vector LN = normalize (L);
	    float cos_theta_i = LN . N;
	    if (cos_theta_i > 0.0) 
			{
			vector H = normalize (V + LN);
			float rho = exp (-2 * (sqr(X.H) + sqr(Y.H)) / (1 + H.N))
		    / sqrt (cos_theta_i * cos_theta_r);
			C += Cl * (  cos_theta_i * rho);
			}
    }
    return C / (4 * xroughness * yroughness);
}



surface WardAnistropic(float Ka=0.5;
				  float Kd=1.0;
				  float xroughness=0.5;
					float yroughness=0.5;
				  float Ks=0.5;
				)
{
/* init the shader values */
normal Nf = faceforward(normalize(N),I);
vector V = -normalize(I);

/* now calculate the shading values */

color spec = LocIllumWardAnisotropic (Nf, V, normalize(dPdu), xroughness, yroughness);
	
Oi=Os;
Ci= Oi *Cs *(Ka*ambient() + Kd*diffuse(Nf) + Ks*spec);	

}