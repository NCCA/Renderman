surface SurfaceShader(float Kd = 0.5,

     snow_ht = 0.0;

     color snow_color = 1,

     ground_color = color(0.466,0.388,0.309)

                        )

{

vector  n = normalize(N),

        nf = faceforward(n, I);

float   height = 0;

color surfcolor;

Oi = Os;

/* Add snow according to the bump height */

if(displacement("hump", height) == 1)

    {

    float blend =

     smoothstep(snow_ht-0.05,snow_ht+0.05,height);

    surfcolor = mix(ground_color,snow_color,blend); 

    }

  

color  diffusecolor = Kd * diffuse(nf)+surfcolor; 

Ci = Oi * Cs * diffusecolor;

}