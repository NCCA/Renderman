/************************************************************************
 * Orange slice shader, adapted from starball.sl - 
 * Reference:
 *   _Advanced RenderMan: Creating CGI for Motion Picture_, 
 *   by Anthony A. Apodaca and Larry Gritz, Morgan Kaufmann, 1999.
 ************************************************************************/
#include "filterwidth.h"
/* Use signed Perlin noise */
#define snoise(x) ((2*noise(x))-1)


#define pulse(a,b,fuzz,x) (smoothstep((a)-(fuzz),(a),(x)) - \
                           smoothstep((b)-(fuzz),(b),(x)))
#define blend(a,b,x) ((a) * (1 - (x)) + (b) * (x))

surface slicedOrange (float Ka=1, Kd=0.95, Ks = 1, roughness=.1; color specularcolor =(1,1,1);) 
{	
	
	
	/* init the shader values */
	normal Nf = faceforward(normalize(N),I);
	vector V = -normalize(I);
	
	
	
	float roughnessTwo = 0.01;
	float Scale=0.04;
	float Layers=4;
	float StartFreq=4;
	float gain=4;
	float lacunarity=1.9132;
	string noiseSpace="shader";
	
	
	/* here we do the texturing */
	float a;
	float mag=0;
	float freq=StartFreq;
	point PPPPP=transform(noiseSpace,P);
	PPPPP*=Scale;
	
	for(a=0; a<Layers; a+=1)
		{
		mag+=abs(float noise(PPPPP*freq)-0.5)*2/freq;
		freq*=lacunarity;
		
		
		}
	// now calculate the shading values 
	mag=smoothstep(0,0.4,mag);


	color segment= color (0.65,0.31,0.01);
	float baseColorFrequency = 1;
	
	// create variations of the baseColor to pass it to the spline function
 	color darkOrange = segment - 0.025;
	color littleDarkerOrg = segment - 0.0125;
 	color middleOrange = segment;
 	color littleLighterOrg = segment + 0.0125;
 	color LightOrange = segment + color (0.025,0.025,0);
	float valueOne;
	
	float turbfreq = 16;
  	point PPPP;
  	float width, cutoff, fade, f, turb;
  	float maxfreq = 32;

	PPPP = transform("shader", P) * turbfreq;
	
	width = filterwidthp(PPPP);
	cutoff = clamp(0.5 / width, 0, maxfreq);
	
	turb = 0;
	for (f = 1; f < 0.5 * cutoff; f *= 2) 
		turb += abs(snoise(PPPP * f)) / f;
	
	fade = clamp(2 * (cutoff - f) / cutoff, 0, 1);
	turb += fade * abs(snoise(PPPP * f)) / f;
	
	valueOne = turb;
	color segmentColor;
	// use the spline function to color the base of the orange  
 			segmentColor = spline(valueOne,darkOrange
               ,littleDarkerOrg
               ,middleOrange
               ,littleLighterOrg
               ,littleLighterOrg
               ,middleOrange
               ,littleDarkerOrg
               ,middleOrange
               ,littleLighterOrg
               ,LightOrange);
// ***********************************************************

	
	float txtscaleIS = 4;
	float octavesIS = 8, omegaIS = 0.35, lambdaIS = 2;
	float thresholdIS = 0;
	
	color interiorSkin;
	color baseColor= color (0.72,0.61,0.18);
	float baseColorFrequency1 = 1;
	
	// create variations of the baseColor to pass it to the spline function
 	color darkOrange1 = baseColor - 0.025;
	color littleDarkerOrg1 = baseColor - 0.0125;
 	color middleOrange1 = baseColor;
 	color littleLighterOrg1 = baseColor + 0.0125;
 	color LightOrange1 = baseColor + color (0.025,0.025,0);
	float valueTwo;
	
	float turbfreq1 = 16;
  	point PPPP1;
  	float width1, cutoff1, fade1, f1, turb1;
  	float maxfreq1 = 32;

	PPPP1 = transform("shader", P) * turbfreq1;
	
	width1 = filterwidthp(PPPP1);
	cutoff1 = clamp(0.5 / width1, 0, maxfreq1);
	
	turb1 = 0;
	for (f1 = 1; f1 < 0.5 * cutoff1; f1 *= 2) 
		turb1 += abs(snoise(PPPP1 * f1)) / f1;
	
	fade1 = clamp(2 * (cutoff1 - f1) / cutoff1, 0, 1);
	turb1 += fade1 * abs(snoise(PPPP1 * f1)) / f1;
	
	valueTwo = turb1;
	// use the spline function to color the base of the orange  
 			interiorSkin = spline(valueTwo,darkOrange1
               ,littleDarkerOrg1
               ,middleOrange1
               ,littleLighterOrg1
               ,littleLighterOrg1
               ,middleOrange1
               ,littleDarkerOrg1
               ,middleOrange1
               ,littleLighterOrg1
               ,LightOrange1);
	
	PPPP=P- valueOne*Nf*0.01;
	N= calculatenormal(PPPP);
	Nf = faceforward(normalize(N),I);		   
			   
	float txtscale = 1;	   
	float octaves = 6, omega = 0.35, lambda = 2;
	float threshold = 0;
	   
	float value;
  	point PPP;      
  	float i, total, frequency, amp;

 	 PPP = txtscale * transform ("shader", P);

  	value = 0;
  	frequency = 20;  amp = 0.5;  total = 0;
  	for (i = 0;  i < octaves;  i += 1) {
      total += amp * snoise (PPP*frequency);
      frequency *= 4.222;  amp *= omega;
    }
	value = total;
	float scale = 2;

	point PP = normalize(transform("shader", P));
	
	float smallnoise;
	float bignoise;
	smallnoise = noise(2 * PP);
	bignoise = noise(0.05 * PP);
	
    float ddv = 10*abs(dv);
    float ddu = (25*abs(du));//*valueOne
	
    float ang = (mod (s*360, 144))+0.000001; //curvature
	
    float ht = .3090/sin(((ang+18)*.01745));//how many times the wave repeats
	
    ang = mod ((1-s)*360, 144);//curvature
	
	float ht1 = .3090/sin(((ang+18)*.01745));//lower band
	
	ang = mod (s*10, 2); //segs
	
	
//	Segment fillets
color surface_color, layer_color;
  color surface_opac, layer_opac;
  float sss, ttt;
  point center;
  float radiusTwo, widthTwo;
  float d;
  float noi;
  float fuzz = 0.1;
  float freqTwo = 6;
  color ringcolor = segmentColor-0.060;
  float noifreq = 30;
  float noiscale = 0.4;
	float stretch = 5.5;
  /* init */

  surface_color = segmentColor+0.045;
  surface_opac = interiorSkin+0.045;

  /* compute base noise based on texture coords */

  noi = noise(s * noifreq, t * noifreq);

  /* perturb ss, tt */

  sss =  ((s*stretch) + snoise(noi + 912) * noiscale);
  ttt = ((t) + snoise(noi + 333) * noiscale);

  /* repeated rings */

  sss = mod(sss*freqTwo,1);
  ttt = mod(ttt*freqTwo,1);

  center =point "shader" (0.5, 0.5, 0);  /* position of ring */
  radiusTwo = 0.50;           /* radius of ring */
  widthTwo = 0.1;             /* width of ring */
  point here = point(sss,ttt,0);
  d = distance(center, here);
  layer_color = ringcolor;
  layer_opac = pulse(radiusTwo - widthTwo / 0.6, radiusTwo + widthTwo / 1, fuzz, d);
  surface_color = blend(surface_color, layer_color, layer_opac);

color lines=surface_color;



	/****************************************************/
	
	//color lines = mix(color(0,0,0),color(0,0,0),ang);
	
    ht = max (ht, ht1);	//how many times the wave repeats
	
    ht1 = ht*.5-min(t*2, 1);	//gets rid of the top row of waves 
	
    ht1 = clamp (ht1, -ddu, ddu)/(ddu*2)+.5;//color clamping of top waves
	
    ht = (ht/2 - min((1-t)*2, 1));//gets rid of the bottom waves(star) by color clamping 
	
    ht1 = ht1 + clamp(ht, -ddu, ddu)/(ddu*2)+.5;//gets rid of bottom waves

	
	
    //color Ct = mix (color(.8,.6,0), color (.5,.05,.05), ht1);
	color Ct = mix (lines, interiorSkin , ht1);
	
	float htC = (ht/2 - min((1-t)*2, 1));//gets rid of the bottom waves(star) by color clamping 
	
    float ht1C = ht1 + clamp(ht, -ddu, ddu)/(ddu*2)+.5;//gets rid of bottom waves
	
	Ct = mix (lines-0.08, interiorSkin-0.08, ht1C-0.08);
    //Ct = mix (color(0,0.2,.7), Ct, clamp(abs(t-0.5)-0.1, 0, ddv)/ddv);
	
	
	float tt = clamp(abs(t-0.05*value)-0.025, 0, ddv)/ddv;//-0.1 ..
	
   Ct = mix (segmentColor, Ct, tt);//-0.5....(0,0.2,.7)
	
	float repeatCount = 5;

   	float fuzzy = 0.045;
	float ssss = mod(repeatCount*s,1)+fuzzy;
    float tttt = t;
    
	color colorLine = interiorSkin;;
    if(ssss<0.08)
		if(tttt>0.2)
		{
			Ct = colorLine; 	
		}
    else
	
	

	
    Nf = faceforward (normalize(N), I);
	Oi=Os;
	Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) + specularcolor * Ks  * specular(Nf,V,roughness));
   
}
