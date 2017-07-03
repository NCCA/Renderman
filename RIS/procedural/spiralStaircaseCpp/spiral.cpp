#include <iostream>
#include <string>
#include <regex>
#include <iterator>
#include <algorithm>
#include <fstream>
#include <ios>
/*
# Signal to prman that we have finished (\377) and
# print out error message on stderr
*/
void niceExit(const std::string &_message) 
{
  std::cerr<<_message;
  //flush stream so prman knows we are done
  std::cout<<'\377';
  std::cout<<std::flush; 
  exit(EXIT_FAILURE);
}	

void block(float _w, float _h, float _d)
{
  std::cout<<"TransformBegin\n";
	float w=_w/2.0f;
	float h=_h/2.0f;
	float d=_d/2.0f;
	//#rear face
	std::cout<<"Translate "<<w<<' '<<h<<" 0\n";
	std::cout<<"\tPatch 'bilinear' 'P' [" << -w<<' '<< -h<<' '<<d<<' '
                                      << -w<<' '<<  h<<' '<<d<<' '
                                      <<  w<<' '<< -h<<' '<<d<<' '
                                      <<  w<<' '<<  h<<' '<<d<<"]\n";
  																	

								
//	#front face
	std::cout<<"\tPatch 'bilinear' 'P' [" << -w<<' '<< -h<<' '<<-d<<' '
                                      << -w<<' '<<  h<<' '<<-d<<' '
                                      <<  w<<' '<< -h<<' '<<-d<<' '
                                      <<  w<<' '<<  h<<' '<<-d<<"]\n";
  
	// #left face
	std::cout<<"\tPatch 'bilinear' 'P' [" << -w<<' '<< -h<<' '<<-d<<' '
                                      << -w<<' '<<  h<<' '<<-d<<' '
                                      << -w<<' '<< -h<<' '<< d<<' '
                                      <<  -w<<' '<< h<<' '<< d<<"]\n";
  
	// #right face
	std::cout<<"\tPatch 'bilinear' 'P' [" <<  w<<' '<< -h<<' '<<-d<<' '
                                      <<  w<<' '<<  h<<' '<<-d<<' '
                                      <<  w<<' '<< -h<<' '<< d<<' '
                                      <<  w<<' '<<  h<<' '<< d<<"]\n";
  
 								
	// #bottom face
	std::cout<<"\tPatch 'bilinear' 'P' [" <<  w<<' '<< -h<<' '<< d<<' '
                                      <<  w<<' '<< -h<<' '<<-d<<' '
                                      << -w<<' '<< -h<<' '<< d<<' '
                                      << -w<<' '<< -h<<' '<<-d<<"]\n";

								
	
	// #top face
	std::cout<<"\tPatch 'bilinear' 'P' [" <<  w<<' '<<  h<<' '<< d<<' '
                                      <<  w<<' '<<  h<<' '<<-d<<' '
                                      << -w<<' '<<  h<<' '<< d<<' '
                                      << -w<<' '<<  h<<' '<<-d<<"]\n";

									
	std::cout<<"TransformEnd\n";

}


int main()
{
  // string to store the arguments sent from prman
  std::string args;
  // regex for removing whitespace from input.
  std::regex ws_re("\\s+"); // whitespace
  // so we need to loop until no input on cin.
  while(  std::getline(std::cin, args))
  {
    // this will store the input tokens for conversion later
    // if we need to do arithmetic on them they will need conversion
    std::vector<std::string> tokens;

    // copy the tokens into a vector
    std::copy( 
              std::sregex_token_iterator(args.begin(), 
              args.end(), ws_re, -1),
              std::sregex_token_iterator(),
              std::back_inserter(tokens)
              );
    // ensure we got enough tokens for this demo
    if(tokens.size() <6)
    {
      niceExit("Error in ribfile not enough arguments");
    }
    float width=std::stof(tokens[1]);
    float height=std::stof(tokens[2]);
    float depth=std::stof(tokens[3]);
    float stairHeight=std::stof(tokens[4]);
    float rotationAngle=std::stof(tokens[5]);

    // Now we will output the cylinder for the center.
    //  # do an explicit TransformBegin
    std::cout<<"TransformBegin\n";
    //			# now the center cylinder
    std::cout<<"\tTranslate 0 -1 0\n";
    std::cout<<"\tRotate -90 1 0 0\n";
    //			size=StairHeight+(3*height)
    std::cout<<"\tCylinder 0.2 "<< stairHeight<< " 1 360\n" ;
    std::cout<<"TransformEnd\n";


  // # now we do some calculations and make our spiral
    float i=0.0f;
    std::cout<<"TransformBegin\n";
    // # loop and build the blocks
    while (i <stairHeight)
    {
      block(width,height,depth);
      std::cout<<"\tTranslate 0 "<<height<<" 0\n";
      std::cout<<"\tRotate "<<rotationAngle<<" 0 1 0\n";
      i+=height;
    }
    std::cout<<"TransformEnd\n";

  //flush stream so prman knows we are done
    std::cout<<'\377';
    std::cout<<std::flush; 
    args.clear();
  }
}