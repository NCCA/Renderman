/*Last Update 12 Jan 2009 */
/*Created by: KK YEUNG*/

#include "AOVoutputs.h"

surface AOVplastic(
		color SurfaceColor = 0.5;
		color Transparency = 1;
		float Ka = 0.1;
		float Kd = 0.5;
		color Specularcolor = 1;
		float Ks = 0.5;
		float roughness = 0.1;
		float Kr = 0.3;
		float Kp = 1; /*bounce light intensity */
		float indirectDiffuseSample = 100;
		ALLAOV;)
{

		normal Nf = faceforward( normalize(N), I);
		vector V = -normalize(I);
	
		vector R = normalize(reflect(I,Nf));
		color Cr = trace(P,R);
		color Ct = SurfaceColor;

		
	
		/*assign different passes to the output */
		Oopacity = Oi = Transparency;
			

			/*premultiply each ouput by Oi*/
			Oambient = Ct * Ka * ambient() * Oi;
			Odiffuse = Ct * Kd * diffuse(Nf) * Oi;
			Obounce = Ct * Kp * indirectdiffuse(P,Nf,indirectDiffuseSample) * Oi;
			Ospecular = Specularcolor * Ks * specular(Nf, V, roughness) * Oi;
			Oreflect = Specularcolor * Cr * Kr * Oi;
	
		/*beauty pass*/
		Ci = (Oambient + Odiffuse + Obounce) + Ospecular + Oreflect;



		/*Surface Normal for compositing*/
		OwsNormal = worldSurfaceNormal(Nf) * Oi;

		/*vector from Surface to Camera */
		OwsCamera = worldSurfaceToCamera(V) * Oi;

		/*world position of Point on Surface */	
		/* P is in camera space by default*/
		point Pw = transform( "world", P );	
		OwsPtPos = color "rgb" (comp(Pw,0),comp(Pw,1),comp(Pw,2));
		OwsPtPos = OwsPtPos * Oi;
}
