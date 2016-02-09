displacement SimpleDisplacement(
		float dispScale=0.04; 
		float RepeatS=4; 
		float RepeatT=4;
		float trueDisp=1;

)
{
// make a copy of the normal 
normal NN = normalize(N);
point PP;

// now calculate the new disp value for P 
float ss=mod(s*RepeatS,1);
float tt=mod(t*RepeatT,1);

float disp=sin(ss*2*PI)*sin(tt*2*PI);
PP=P-NN*disp*dispScale;
N=calculatenormal(PP);
if(trueDisp == 1)
	P=PP;

}




