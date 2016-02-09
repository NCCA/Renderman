/***************** Orange Shader Created by Colm Doherty **************************/


surface orange	(	uniform float Ka = 1;
					uniform float Kd = 0.95;
					uniform float Ks = 1;
					color specularcolor = 1;
					float roughness = 0.21;
					
					//color baseColor= color (0.63,0.25,0.007);
					
					/*  Layer 1 - Parmaters  */
					color baseColor= color (0.72,0.33,0.007);
					color baseColorTwo= color (0.9,0.30,0.023);
					color baseColorFour= color (0.75,0.27,0.023);
		   			float baseColorFrequency = 2;
					
					/*  Layer 2 - Parmaters  */
					
 					color DiskColour = color "rgb" (1,1,1);
 					
					float fuzz= 0.1;
 					
 					float RepeatS=40.21;
 					float RepeatT=35.25;
					
					float scaling = 0.1;
					float colorScale =  0.115;
					color drkOrgSpotsColor = color (0.65,0.23,0.005) ;
					
					/* Layer 3 - Parmaters */
					
 					color DiskColour3 = color "rgb" (1,1,1);
 					
					float fuzz3= 0.15;
 					
 					float RepeatS3=50.25;
 					float RepeatT3=45.21;
					
					float scaling3 = 0.1;
					float colorScale3 =  0.115;
					color drkOrgSpotsColorIncrease = color (0.55,0.20,0.05) ;
					
					
				)
					
			{
			/* Initialize shader variables */
			/* init the shader values */
			
			normal Nf = faceforward(normalize(N),I);
			vector V = -normalize(I);
			color cs;
			color css;
			//normal Nf = normalize(faceforward(N, I));
			//color Ct;
			
 			
			
			
			
			/************************
 			* 
  			* Layer 1 - Base color 
  			*
  			************************/
			
			 /* Transform P from "current" to "shader" */
 			point PP = transform("shader", P) * baseColorFrequency;
			
			/*calculate a very simple noise to drive the spline function */
 			float simpleNoise = float noise(2 * PP);
			
			
			float biggerNoise = float noise(11 * PP);
			
			
			 /* create variations of the baseColor to pass it to the spline function*/
 			color darkOrange = baseColor - 0.025;
			color littleDarkerOrg = baseColor - 0.0125;
 			color middleOrange = baseColor;
 			color littleLighterOrg = baseColor + 0.0125;
 			color LightOrange = baseColor + color (0.025,0.025,0);

 			/* use the spline function to color the base of the orange  */
 			cs = spline(simpleNoise,darkOrange
               ,littleDarkerOrg
               ,middleOrange
               ,littleLighterOrg
               ,littleLighterOrg
               ,middleOrange
               ,littleDarkerOrg
               ,middleOrange
               ,littleLighterOrg
               ,LightOrange);
			
			 color Ct=cs;
			/******************************
  			*
  			* Layer 2 - Dark orange noisy spots 
 			*
  			*******************************/
			/* texturing of spots */
			
			
			
			point center = (point(0.4,0.3,0.4)*simpleNoise);
			float ss=mod(s*RepeatS,1);
			float tt=mod(t*RepeatT,1);
			point here = point(ss,tt,0);
			setcomp(here,2,comp(center,2));
			
			float dist=distance(center,here);
			
			float stCellnoise =float cellnoise(RepeatS*s,RepeatT*t)*scaling;
			
			//float inDisk=1-smoothstep(radius-fuzz,radius+fuzz,dist);
			
			float inDisk=1-smoothstep(stCellnoise-fuzz,stCellnoise+fuzz,dist);
			
			color dOSColor = drkOrgSpotsColor - colorScale;
			
			color cs2 = mix(Ct,dOSColor+0.2,inDisk);
			
			Ct=cs2;
			
			PP=P- inDisk*Nf*0.1;
			N= calculatenormal(PP);
			Nf = faceforward(normalize(N),I);
			
			
			/******************************
  			*
  			* Layer 3 - Darker orange noisy spots / scratches 
 			*
  			*******************************/
			point center3 = (point(0.59,0.611,0.1)*biggerNoise);
			float ss3=mod(s*RepeatS3,1);
			float tt3=mod(t*RepeatT3,1);
			point here3 = point(ss3,tt3,0);
			setcomp(here3,2,comp(center3,2));
			
			float dist3=distance(center3,here3);
			
			float stCellnoise3 =float cellnoise(RepeatS3*s,RepeatT3*t)*scaling3;
			
			//float inDisk=1-smoothstep(radius-fuzz,radius+fuzz,dist);
			
			float inDisk3=1-smoothstep(stCellnoise3-fuzz3,stCellnoise3+fuzz3,dist3);
			
			color dOSColor3 = drkOrgSpotsColorIncrease - colorScale3;
			
			color cs3 = mix(Ct,dOSColor3,inDisk3);
			
			
			PP=P- inDisk3*Nf*0.0049;
			N= calculatenormal(PP);
			Nf = faceforward(normalize(N),I);
			
			Ct = cs3;
				/******************************
  			*
  			* Layer 4 - Darker orange color / scratches 
 			*
  			*******************************/
			
			
			color DdarkOrange = baseColorFour - 0.025;
			color DlittleDarkerOrg = baseColorFour - 0.0125;
 			color DmiddleOrange = baseColorFour;
 			color DlittleLighterOrg = baseColorFour + 0.0125;
 			color DLightOrange = baseColorFour + color (0.025,0.025,0);

 			/* use the spline function to color the base of the orange  */
 			color cs4 = spline(biggerNoise,DdarkOrange
               ,DlittleDarkerOrg
               ,DmiddleOrange
               ,DlittleLighterOrg
               ,DlittleLighterOrg
               ,DmiddleOrange
               ,DlittleDarkerOrg
               ,DmiddleOrange
               ,DlittleLighterOrg
               ,DLightOrange);
			
			Ct = cs4;			
			
			
			Oi=Os;
			Ci= Oi * (Ct * (Ka * ambient() + Kd *diffuse(Nf)) + 
			specularcolor * Ks  * specular(Nf,V,roughness));
			
}

