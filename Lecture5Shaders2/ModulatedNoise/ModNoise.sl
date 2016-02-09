surface ModNoise

(

 float Ka=1;float roughness = 0.01;
 float RepeatS=1;  float RepeatT=1;
 float Frequency=1; 
 float Ks=0.1;
 float Kd=1;
 vector NoiseVec=vector (1,0,0);

)

{

/* init the shader values */

normal Nf = faceforward(normalize(N),I);

vector V = -normalize(I);

/* here we do the texturing */

// create repeats

point PP = transform("shader",P);

normalize(NoiseVec);

float ss=s+ float noise(PP*RepeatS)*Frequency;

float tt=t+ float noise((PP*RepeatT) + NoiseVec)*Frequency;

// now set the colour based on the noise function

color Ct= cellnoise(ss*Frequency,tt*Frequency);

/* now calculate the shading values */

Oi=Os;

Ci= Oi * (Ct * (Ka * ambient() + Kd*diffuse(Nf)) + Ks*specular(Nf,V,roughness));

}