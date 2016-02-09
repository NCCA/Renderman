surface Noise

(

 float Ka=1; float roughness = 0.01;

 float RepeatS=1; float RepeatT=1; float Frequency=1;

)

{

/* init the shader values */

normal Nf = faceforward(normalize(N),I);

vector V = -normalize(I);

// create repeats

float ss=mod(s,RepeatS);

float tt=mod(t,RepeatT);

// transform the current point into shader space

// this creates a solid texture

point Np= transform("shader",P); 

// now set the colour based on the noise function

color Ct= noise(Np*Frequency);

/* now calculate the shading values */

Oi=Os;

Ci= Oi * (Ct * (Ka * ambient() + diffuse(Nf)) +

specular(Nf,V,roughness));

}