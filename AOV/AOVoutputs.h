/*Last Update : 12 Jan 2008*/
/*Created by KK YEUNG*/

#ifndef __AOVOUTPUTS_H__
#define __AOVOUTPUTS_H__

#define ALLAOV\
		output varying color Oambient = 0;\
		output varying color Oreflect = 0;\
		output varying color Ospecular = 0;\
		output varying color Odiffuse = 0;\
		output varying color Oopacity = 0;\
		output varying color Obounce = 0;\
		output varying color OwsNormal = 0;\
		output varying color OwsCamera = 0;\
		output varying color OwsPtPos = 0;

#endif



color worldSurfaceNormal(normal i_Nf)
{
	color o_C = (0,0,0);

	/*get the normalized normal out in "world" space*/
	/*Since we want all the suface normal pointing towards	*/
	/*the camera, so we use Nf instead of N			*/
	
	normal NN = normalize( ntransform( "world", i_Nf));								
	vector N_remap = 0.5 * (vector(1,1,1) + NN);			/*remap the range from (-1,1) to (0,1)*/
	o_C = color "rgb" (comp(N_remap,0),comp(N_remap,1),comp(N_remap,2));
	
	return o_C;	
}

color worldSurfaceToCamera( normal i_V)
{
	color o_C = (0,0,0);

	/*normal NN = normalize( ntransform( "world", i_V));*/
	vector N_remap = 0.5 * (vector(1,1,1) + i_V);			/*remap the range from (-1,1) to (0,1)*/
	o_C = color "rgb" (comp(N_remap,0),comp(N_remap,1),comp(N_remap,2));
	
	return o_C;	

}
