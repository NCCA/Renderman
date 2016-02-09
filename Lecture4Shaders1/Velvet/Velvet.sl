#define SQR(A) ((A)*(A))

surface Velvet (float Ka = 0.05,
              Kd = 0.1,
              Ks = 0.1;
	    float backscatter = 0.1,
	    edginess = 10;
        color sheen = .25;
        float roughness = .1;
  )
{
  normal Nf;                     /* Normalized normal vector */
  vector V;                      /* Normalized eye vector */
  vector H;                      /* Bisector vector for Phong/Blinn */
  vector Ln;                     /* Normalized vector to light */
  color shiny;                   /* Non-diffuse components */
  float cosine, sine;            /* Components for horizon scatter */

  Nf = faceforward (normalize(N), I);
  V = -normalize (I);

  shiny = 0;
  illuminance ( P, Nf, PI/2.0 ) {
    Ln = normalize ( L );
    /* Retroreflective lobe */
    cosine = max ( Ln.V, 0 );
    shiny += pow ( cosine, 1.0/roughness ) * backscatter
      * Cl * sheen;
    /* Horizon scattering */
    cosine = max ( Nf.V, 0 );
    sine = sqrt (1.0-SQR(cosine));
    shiny += pow ( sine, edginess ) * Ln.Nf * Cl * sheen;
  }

  Oi = Os;
  /* Add in diffuse color */
  Ci = Os * (Ka*ambient() + Kd*diffuse(Nf)) * Cs + shiny;

}



