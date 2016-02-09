/* Use signed Perlin noise */
#define snoise(x) ((2*noise(x))-1)


displacement orangeDisp (	float txtscale = 1;
	    			float octaves = 4, omega = 0.35, lambda = 2;
	    			float threshold = 0;
					float Km = 0.07;
	     )
{
  float value;
  point PP;      /* Surface point in shader space */
  float i, total, frequency, amp;

  PP = txtscale * transform ("shader", P);

  /* Use fractional Brownian motion to compute a value for this point */
/*  value = fBm (PP, omega, lambda, octaves); */
  value = 0;
  frequency = 0.5;  amp = 0.5;  total = 0;
  for (i = 0;  i < octaves;  i += 1) {
      total += amp * snoise (PP*frequency);
      frequency *= 4.222;  amp *= omega;
    }
  value = total;

    P += Km * value * normalize(N);
	N = calculatenormal(P);
}








