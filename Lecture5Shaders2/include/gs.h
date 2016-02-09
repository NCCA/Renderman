/*
** gs.h
** contains useful macros.
*/
/*-----------------------------------------------------------------*/

#define gs_AA(x) (abs(Du(x)*du) + abs(Dv(x)*dv))
#define gs_sq(x) 		(x * x)
#define gs_square(x) ((x)*(x))
#define gs_cube(x) 		((x)*(x)*(x))
#define gs_quad(x) 		((x)*(x)*(x)*(x))
#define gs_shift(x) 		((x+1)/2)
#define gs_radius(a,b) 	(sqrt(a*a+b*b))
#define gs_aasize(x) 	(max(length(Du(x)*du),length(Dv(x)*dv)))
#define gs_blend(b,w,x) 	(smoothstep(b-w,b+w,x))
#define gs_luminence(c) 	((comp(c,0)+comp(c,1)+comp(c,2))/3)
#define gs_lum(c) 	((comp(c,0)+comp(c,1)+comp(c,2))/3)
#define gs_snoiseC(c) 	(2* color noise(c) - 1)
#define gs_snoiseP(p) 	(2* point noise(p) - 1)
#define gs_snoiseV(v) 	(2*vector noise(v) - 1)
#define gs_snoiseN(n) 	(2*normal noise(n) - 1)
#define gs_snoise(a)  	(2* float noise(a) - 1)
#define gs_snoiseT(p,t) 	(2*noise(p,t)-1)
#define gs_bias(x,b) 	(pow(x,log(b)/log(0.5))
#define gs_blendwidth(x,y) 	(floor(x)*(1-2*y)+max(0,mod(x,1)-y))
#define gs_fuzzy(a,b,zz,x) 	(smoothstep(a-zz,a,x)*(1-smoothstep(b,b+zz,x)))
#define gs_filterwidth(x) 	(max((abs(Du(x)*du)+abs(Dv(x)*dv)),MINFILTERWIDTH))
#define gs_filteredpulse(a,b,x,w) (max(0,(min(x-w/2,a)-max((x-w/2)+w,b))/w))
#define gs_ripples(a,b,x,y,w) (gs_shift(cos((2*PI*w)+2*\
		PI*gs_radius(a*(x-.5),b*(y-.5)))))
#define gs_pulse(B,W,X) \
	(smoothstep(0.5-(B)-(W), 0.5-(B),     X) - \
	 smoothstep(0.5+(B)    , 0.5+(B)+(W), X))
#define gs_FUZ(x,aa) ((smoothstep(0.5,0.5+aa,x))+(1-smoothstep(0,aa,x)))
#define gs_BLEND(x,y) (((x)*(y))+((1-(x))*(1-(y))))
#define gs_skin(fx,fy,x,y) (gs_sq(noise((gs_shift(sin(PI*fx*x)) + \
					 gs_shift(cos(PI*fy*y)))/ 2)))
/*-----------------------------------------------------------------*/
#define GS_AA(x) (abs(Du(x)*du) + abs(Dv(x)*dv))
#define GS_sq(x) 		((x)*(x))
#define GS_square(x) ((x)*(x))
#define GS_cube(x) 		((x)*(x)*(x))
#define GS_quad(x) 		((x)*(x)*(x)*(x))
#define GS_shift(x) 		((x+1)/2)
#define GS_radius(a,b) 	(sqrt(a*a+b*b))
#define GS_aasize(x) 	(max(length(Du(x)*du),length(Dv(x)*dv)))
#define GS_blend(b,w,x) 	(smoothstep(b-w,b+w,x))
#define GS_luminence(c) 	((comp(c,0)+comp(c,1)+comp(c,2))/3)
#define GS_lum(c) 	((comp(c,0)+comp(c,1)+comp(c,2))/3)
#define GS_snoiseC(c) 	(2* color noise(c) - 1)
#define GS_snoiseP(p) 	(2* point noise(p) - 1)
#define GS_snoiseV(v) 	(2*vector noise(v) - 1)
#define GS_snoiseN(n) 	(2*normal noise(n) - 1)
#define GS_snoise(a)  	(2* float noise(a) - 1)
#define GS_snoiseT(p,t) 	(2*noise(p,t)-1)
#define GS_bias(x,b) 	(pow(x,log(b)/log(0.5))
#define GS_blendwidth(x,y) 	(floor(x)*(1-2*y)+max(0,mod(x,1)-y))
#define GS_fuzzy(a,b,zz,x) 	(smoothstep(a-zz,a,x)*(1-smoothstep(b,b+zz,x)))
#define GS_filterwidth(x) 	(max((abs(Du(x)*du)+abs(Dv(x)*dv)),MINFILTERWIDTH))
#define GS_filteredpulse(a,b,x,w) (max(0,(min(x-w/2,a)-max((x-w/2)+w,b))/w))
#define GS_ripples(a,b,x,y,w) (gs_shift(cos((2*PI*w)+2*\
		PI*gs_radius(a*(x-.5),b*(y-.5)))))
#define GS_pulse(B,W,X) \
	(smoothstep(0.5-(B)-(W), 0.5-(B),     X) - \
	 smoothstep(0.5+(B)    , 0.5+(B)+(W), X))
#define GS_FUZ(x,aa) ((smoothstep(0.5,0.5+aa,x))+(1-smoothstep(0,aa,x)))
#define GS_BLEND(x,y) (((x)*(y))+((1-(x))*(1-(y))))
#define GS_skin(fx,fy,x,y) (GS_sq(noise((GS_shift(sin(PI*fx*x)) + \
					 GS_shift(cos(PI*fy*y)))/ 2)))
/*-----------------------------------------------------------------*/

/*#define PI 3.14159265358979323846*/
#define MINFILTERWIDTH 1.0e-6
#define GS_MINFILTERWIDTH 1.0e-6
#define PULSE(a,b,x) (step((a),(x)) - step((b),(x)))
#define boxstep(a,b,x) clamp(((x)-(a))/((b)-(a)),0,1)
#define M_PI		3.14159265358979323846
#define snoisexy(x,y) (2 * (float noise(x,y)) - 1)
#define vsnoise(p) (2 * (vector noise(p)) - 1)
/*-----------------------------------------------------------------*/

/*-----------------------------------------------------------------*/
/*
** Useful functions.
** Author: Liza Keith, liza@cinegrfx.com, Copyright (c) 1996 Cinema Graphics, Inc. 
*/
/*-----------------------------------------------------------------*/
#define snoise(a) (2*noise(a)-1)
#define snoiseP(p) (2*point noise(p)-1)
#define blend(b,w,x) (smoothstep(b-w,b+w,x))
#define luminence(c) ((comp(c,0)+comp(c,1)+comp(c,2))/3)
#define snoiseV(a) (2*vector noise(a) - 1)
#define SQRT3 1.7320508
#define fuzzy(a,b,fuzz,x) (smoothstep(a-fuzz,a,x)*(1-smoothstep(b,b+fuzz,x)))

/*-----------------------------------------------------------------*/

float SB_VLNoise(point p;float freq) 
{
    return(snoise(snoiseP(p)+(p*freq)));
}


float SB_beaten(point p; float inc, freq, octaves)
{

    varying float i;
    varying float scale = 1.0;
    varying float chaos = 0.5;
    if ( inc != 0 )
        for (i = 0; i < octaves; i += 1 )
        {
             chaos += snoise(p*freq*scale)/scale;
             scale *= inc;
        }
    return(clamp(chaos,0,1));
}

float SB_brushed(point p; string dir; float freq, size)
{
    varying float scale;
    varying float stroke = 0;
    varying point q = p*freq;
    varying float pixel = sqrt(area(p));

    if ( dir == "z" ) 
        setzcomp(q, zcomp(q)/size);
    else if ( dir == "y" ) 
        setycomp(q, ycomp(q)/size);
    else
        setxcomp(q, xcomp(q)/size);

    for (scale = 1; scale > 2*pixel; scale /= 2) 
        stroke += scale * noise(q/scale);

    if (stroke < 1)
          stroke = (1-smoothstep(0,1,size/pixel)) * (1-stroke) + stroke;

    return(clamp(stroke-.2,0,1));
}


float SB_clampedturb(point p; float freq, maxfreq, dist, mindist, maxdist)
{
  extern  float  du;
  extern  float  dv;
  varying point  q     = p*freq;
  varying vector dPPdu = Du(q)*du;
  varying vector dPPdv = Dv(q)*dv;
  varying float  width = 2*max(length(dPPdu), length(dPPdv));
  varying float  clip  = clamp(0.5/width, 0, maxfreq);
  varying float  sum   = 0;
  uniform float i;
  for (i = 1; i < clip; i *= 2) 
	sum += abs(2*smoothstep(0.25,0.75,noise(q*i))-1)/i;

  float dampen = clamp(2*(clip-i)/clip, 0, 1);
  sum += dampen * abs(2*smoothstep(0.25,0.75,noise(q*i))-1)/i;

  sum = mix(sum, 0.5, smoothstep(mindist, maxdist, dist));

  return(sum);
}


color SB_cartoon ( float Ka,Kd,Ks,lumDiff,LOW,MID,TOP,SPC,FUZ; 
                      color AMB,D1,D2,D3,Spec,HI,OP; )
{

    varying float hilite;
    varying float mixer;
    varying color high;
    varying color med;

    if (lumDiff > (TOP+MID)/2) {
        med   = D2;                             /* medium diffuse color */
        high  = D3;                             /* upper diffuse color */
        mixer = blend(TOP,FUZ,lumDiff);
    } 
    else if (lumDiff > (MID+LOW)/2) {
        med   = D1;                             /* lower diffuse color */
        high  = D2;                             /* medium diffuse color */
        mixer = blend(MID,FUZ,lumDiff);
    } 
    else {
        med   = AMB;                            /* ambient contribution */
        high  = D1;                             /* lower diffuse color */
        mixer = blend(LOW,FUZ,lumDiff);
    }

    hilite = luminence(Spec);
    return(OP * ((Ka * AMB) + 
                 (Kd * mix(med,high,mixer))) + 
                 (Ks * HI * Spec * blend(SPC,FUZ,hilite)));
}


float SB_cloudy(point p; float base, freq, octaves)
{
    varying float i, sum, size, lacun; 

    sum = 0;
    lacun = 1;
    size = base;
    for (i = 0; i < octaves; i += 1 )
    {
        sum += size * noise(p*freq*lacun);
        size /= 2;
        lacun *= 2;
    }
    return(min(sum/(base+1),1));
}

float SB_dented(point p; float b, fq, it; )
{
    varying float i, sum, freq;

    sum = 0;
    freq = fq;
    for (i=0;i<it;i+=1)
    {
        sum += b*abs(.5-float noise(p*freq))/freq;
        freq *= 2;
    }
    return(sum);
}


float SB_ellipse(point Q;          /* Test point on the x-y plane */
		    float a, b;       /* Inner superellipse */
		    float A, B;       /* Outer superellipse */
		    float roundness;  /* Same roundness for both ellipses */
		   )
{
    float result;
    float x = abs(xcomp(Q)), y = abs(ycomp(Q));
    if (roundness < 1.0e-6) 
    { 					/* Simpler case of a square */
        result = 1 - (1-smoothstep(a,A,x)) * (1-smoothstep(b,B,y));
    } 
    else 
    { 					/* Harder, rounded corner case */
        float re = 2/roundness;   /* roundness exponent */
        float q = a * b * pow (pow(b*x, re) + pow(a*y, re), -1/re);
        float r = A * B * pow (pow(B*x, re) + pow(A*y, re), -1/re);
        result = smoothstep (q, r, 1);
    }
    return result;
}

float SB_feathery(point p; float freq, it)
{

    varying float i, sum, size;

    sum = 0;
    size = 1;
    for (i = 0; i < it; i += 1 )
    {
         sum += snoise(size*p + snoiseV(size*p)*freq)/size;
         size *= 2;
    }
    return(sum*1.4);
}

float SB_furry(float amplitude, freq, S, T; ) 
{
    return(amplitude * noise(sin(freq*S*2*PI)*freq, sin(freq*T*2*PI)*freq));
}

float SB_glow(vector eye, norm; float ramp )
{

    float falloff = normalize(eye).normalize(norm);
    return((falloff > 0) ? pow(falloff,ramp) : 0);
}


float SB_granite(point p; float freq )
{
    varying float pix, sum, oct;
    varying point foo;

    sum = 0;
    foo = p * freq;
    pix = sqrt(area(foo));
    for (oct = 1; oct > 2*pix; oct /= 2) sum += oct * noise(foo/oct);
    if (oct > pix) sum += clamp((oct/pix)-1,0,1) * oct * noise(foo/oct);
    return(sum);
}

float SB_hexagonals(float S, T, radius, mortarwidth, sfuzz, tfuzz )
{
  float width;
  float ss, tt;
  float ttile, stile;
  float x, y;
  float halfwidth;
  float mixer;

  width = radius * SQRT3;

  tt = mod(T, 1.5*radius);
  ttile = floor(T/(1.5*radius));

  ss = (mod(ttile/2, 1) == 0.5) ? S + width/2 : S;
  stile = floor(ss / width);
  ss = mod(ss, width);

  mixer = 0;
  halfwidth = mortarwidth/2;
  if (tt < radius) 
      mixer = 1 - fuzzy(halfwidth,width-halfwidth,-sfuzz,ss);
  else 
  {
      x = width/2 - abs(ss - width/2);
      y = SQRT3 * (tt - radius);
      if (y > x) 
      {
          if (mod (ttile/2, 1) == 0.5) stile -= 1;
          ttile += 1;
          if (ss > width/2) stile += 1;
      }
      mixer = fuzzy(x-SQRT3*halfwidth,x+SQRT3*halfwidth,tfuzz,y);
    }

  return(1 - mixer);
}

float SB_marbled(point p; float freq, slide)
{
    varying float scale;
    varying float chaos = 0;
    varying point q = p*freq;
    varying float pixel = sqrt(area(q));

    for (scale = 1; scale > 2*pixel; scale /= 2) 
        chaos += scale * noise(q/scale);

    if (scale > pixel) 
        chaos += clamp((scale/pixel)-1, 0, 1) * scale * noise(q/scale);

    return(clamp(slide*chaos-(slide-1),0,1));
}



float SB_occlusion(point P1, P2; string coords;
                      float width, height, wedge, hedge, round;
                    )
{
    point  Pb1 = transform(coords, P1);
    point  Pb2 = transform(coords, P2);
    float  zp1 = zcomp(Pb1);
    float  zp2 = zcomp(Pb2);
    float  off = 1;

    /* Blocker works only if it's straddled by ray endpoints. */
    if (zp2*zp1 < 0) 
    {
    	vector dir = Pb1 - Pb2;
        point Q = Pb1 - dir*(zp1/zcomp(dir));
        off *= SB_ellipse(Q,width,height,width+wedge,height+hedge,round);
    }
    return off;
}


float SB_rust(point p; float inc, octaves)
{
    varying float i;
    varying float rusty = 0;
    varying float scale = 1;  
    varying float freq = 1;  

    for (i = 0; i < octaves; i += 1 )
    {
        rusty += snoise(freq*p) * scale;
        scale *= inc;
        freq *= 2;
    }
    return(rusty);
}


#define SB_softn(a,az,b,bz,x) (smoothstep(a-az,a,x)*(1-smoothstep(b,b+bz,x)))

float SB_shapelight(point PL;                     /* Point in light space */
		      string type;                   /* light type */
		      vector axis;                   /* light axis */
		      float znear, zfar;             /* z clipping */
		      float nearedge, faredge;
		      float falloff, falloffdist;    /* distance falloff */
		      float maxint;
		      float shearx, sheary;          /* shear the direction */
		      float width, height;           /* xy superellipse */
		      float fuzziness, roundness;
		      float beamwidth;        	     /* angle falloff */
		      )
{
    /* Examine the z depth of PL to apply 
     * the (possibly smooth) cuton and cutoff.
     */
    float PLlen = length(PL);
    float Pz    = (type == "spot") ? zcomp(PL) : PLlen;
    float atten = SB_softn(znear, nearedge, zfar, faredge, Pz);

    /* Distance falloff */
    if (falloff != 0) 
    {
	float damp = log(1/maxint);
	atten *= (PLlen > falloffdist) ? pow(falloffdist/PLlen, falloff) :
		 (maxint * exp(damp*pow(PLlen/falloffdist, -falloff/damp)));
    }

    /* Clip to ellipse */
    if (type != "omni" && beamwidth > 0)
        atten *= pow(normalize(vector PL).axis, beamwidth);

    if (type == "spot")
        atten *= 1 - SB_ellipse(PL/Pz-point(shearx,sheary,0), width, height,
                             width+fuzziness, height+fuzziness, roundness);
    return atten;
}


float SB_streaked(point p; string axis; float freq, leng, mag; ) 
{
   point q = p;

   if ( axis == "x" ) setxcomp(q,xcomp(p)/leng);
   else if ( axis == "z" ) setzcomp(q,zcomp(p)/leng);
   else setycomp(q,ycomp(p)/leng);

   return(clamp(mag*snoise(freq*q),0,1)); 
}



float SB_turbulence(point p; float base, freq )
{
    varying point q = p;
    varying float sum = 0;
    varying float i;
    for (i = base;i < freq;i *= 2)
    {
        sum += abs(snoise(q))/i;
        q *= 2;
    }
    return(max(0,sum-0.3));
}

point SB_twistedP(point p; float twist;)
{
  point nP;
  float angle;

  nP = normalize(p);
  angle = twist * 2*PI*(xcomp(nP)*xcomp(nP) + ycomp(nP)*ycomp(nP));
  return( point(xcomp(p)*cos(angle) - ycomp(p)*sin(angle),
                ycomp(p)*cos(angle) + xcomp(p)*sin(angle),
                zcomp(p)));
}


float SB_wispy(float x, y, angle, octaves)
{
    varying float i;
    varying float X = x;
    varying float Y = y;
    varying float phase = 0;
    varying float scale = 1;
    varying float chaos = 0;
    varying float incre = 1;
    for (i = 1; i < octaves; i += 1)
    {
         phase  = (PI/2) * sin(PI*Y*scale);
         chaos += incre * sin(phase+2*PI*X*scale);
         incre *= cos(radians(angle));
         scale *= 2;
    }

    return(chaos);
}

/* taken from SGI's /usr/include/math.h - see 'man math' */
#define _SB_E             2.7182818284590452354
#define _SB_LOG2E         1.4426950408889634074
#define _SB_LOG10E        0.43429448190325182765
#define _SB_LN2           0.69314718055994530942
#define _SB_LN10          2.30258509299404568402
#define _SB_PI            3.14159265358979323846
#define _SB_PI_2          1.57079632679489661923
#define _SB_PI_4          0.78539816339744830962
#define _SB_1_PI          0.31830988618379067154
#define _SB_2_PI          0.63661977236758134308
#define _SB_2_SQRTPI      1.12837916709551257390
#define _SB_SQRT2         1.41421356237309504880
#define _SB_SQRT1_2       0.70710678118654752440
#define _SB_PI2           6.28318530717958647692


