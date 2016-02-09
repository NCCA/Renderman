displacement SurfaceBump(float  Km = 0.1,
                               freq = 4;
         output varying float  hump = 0;)

{
vector n = normalize(N);
point PP=  point "object" (P);  
hump = noise(PP * freq);

  
hump = hump - 0.5;
P = P - n * hump * Km;
N = calculatenormal(P);

}