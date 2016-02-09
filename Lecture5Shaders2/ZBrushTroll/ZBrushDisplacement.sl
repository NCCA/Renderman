displacement ZBrushDisplacement(
	float   Km  = 1.0;
    string displace_map="";
	float swidth=0.0001;
	float twidth=0.0001;
	float samples=200;
	)
{
	float   magnitude = 0;
	float	level = 0;
	
if( displace_map != "")	
	{		
	level = float	texture(displace_map,s,t,					
							"swidth", swidth,
							"twidth",twidth,
							"samples", samples);		
	// calculate the displacement
	magnitude = ((level * 2) - 1) * Km;		
	}	
	// no map so don't displace
	else	
		magnitude	= 0.0;	
// calculate the new position
P -= normalize(N) * magnitude;
// re-calc the normal
N=calculatenormal(P);
}
