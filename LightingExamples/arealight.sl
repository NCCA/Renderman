light arealight(color lightcolor = color(1,1,1);
		float intensity = 1;
		string maplist = "";
		float numsamples = 1;
		point Pl1 = point(0, 0, 0);
		point Pl2 = point(0, 1, 0);
		point Pl3 = point(0, 0, 1);
		point Pl4 = point(0, 1, 1);
		float shadowBias = 0.001;
		float gapBias = 0.01) {
    varying float attenuation;

    illuminate ((Pl1+Pl2+Pl3+Pl4)*0.25) {  /* base illumination at average */
                                           /* of light positions           */

    attenuation = shadow(maplist,Ps,"source",Pl1,Pl2,Pl3,Pl4,
              "samples",numsamples, "bias",shadowBias, "gapbias", gapBias);

    Cl = lightcolor * intensity * (1-attenuation);
  }
}