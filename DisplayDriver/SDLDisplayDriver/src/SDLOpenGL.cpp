#include "SDLOpenGL.h"
#include <iostream>

SDLOpenGL::SDLOpenGL(const std::string &_name, int _x, int _y,int _width, int _height, int _ppp)
{
  m_name=_name;
  m_x=_x;
  m_y=_y;
  m_width=_width;
  m_height=_height;
  init();
  if(_ppp ==3)
    m_pixelFormat=GL_RGB;
  else if(_ppp ==4)
    m_pixelFormat=GL_RGBA;
}

void SDLOpenGL::init()
{
  if(SDL_Init(SDL_INIT_EVERYTHING) < 0)
  {
    ErrorExit("Could Not Init Everything");
  }

  m_window=SDL_CreateWindow(m_name.c_str(),m_x,m_y,
                            m_width,m_height,
                            SDL_WINDOW_OPENGL );
  if(!m_window)
  {
    ErrorExit("Could not create Window");
  }

  createGLContext();
  createSurface();
  glEnable(GL_FRAMEBUFFER_SRGB);

}

void SDLOpenGL::updateImage(const float *_image)
{
//  makeCurrent();
//  glBindTexture(GL_TEXTURE_2D, m_texture);

//  glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, m_width, m_height, m_pixelFormat, GL_FLOAT, _image);

  glTexImage2D(GL_TEXTURE_2D, 0, m_pixelFormat, m_width, m_height, 0, m_pixelFormat, GL_FLOAT, _image);
  //glfwSwapBuffers(m_window);
/*
  if(m_update)
  {
    m_update = false;
    glUniform2f(m_trans_uniform, m_trans_x, m_trans_y);
    glUniform1f(m_scale_uniform, m_scale);
  }*/
 // swapWindow();
 // draw();
}

void NGLCheckGLError( const std::string  &_file, const int _line ) noexcept
{
 //std::cout<<"NGLCheckGLError Called ______________________\n";
 auto errNum = glGetError();
  while (errNum != GL_NO_ERROR)
  {
   // std::cout<<errNum<<"\n";
    std::string str;
    switch(errNum)
    {
      case GL_INVALID_ENUM : str="GL_INVALID_ENUM error"; break;
      case GL_INVALID_VALUE : str="GL_INVALID_VALUE error"; break;
      case GL_INVALID_OPERATION : str="GL_INVALID_OPERATION error"; break;
      case GL_OUT_OF_MEMORY : str="GL_OUT_OF_MEMORY error"; break;
      case GL_INVALID_FRAMEBUFFER_OPERATION : str="GL_INVALID_FRAMEBUFFER_OPERATION error";  break;
       // this should be in the spec but it's not on the mac! will check linux
      default : break;
    }
    if(errNum !=GL_NO_ERROR)
    {
      std::cerr<<"GL error "<< str<<" line : "<<_line<<" file : "<<_file<<"\n";
    }
    errNum = glGetError();

   }
}

void printInfoLog(const GLuint &_obj , GLenum _mode=GL_COMPILE_STATUS  )
{
  GLint infologLength = 0;
  GLint charsWritten  = 0;
  char *infoLog;

  glGetShaderiv(_obj, GL_INFO_LOG_LENGTH,&infologLength);
  std::cerr<<"info log length "<<infologLength<<"\n";
  if(infologLength > 0)
  {
    infoLog = new char[infologLength];
    glGetShaderInfoLog(_obj, infologLength, &charsWritten, infoLog);

    std::cerr<<infoLog<<std::endl;
    delete [] infoLog;
    glGetShaderiv(_obj, _mode,&infologLength);
    if( infologLength == GL_FALSE)
    {
      std::cerr<<"Shader compile failed or had warnings \n";
      exit(EXIT_FAILURE);
    }
  }

}
void SDLOpenGL::draw()
{
 glClearColor(0.25f, 0.25f, 0.25f, 1.0f);
 glClear(GL_COLOR_BUFFER_BIT);
 glDrawArrays(GL_TRIANGLES, 0, 6);
 swapWindow();
}

void SDLOpenGL::createSurface()
{
  makeCurrent();
  glGenVertexArrays(1, &m_vao);
  glBindVertexArray(m_vao);

  float vertices[] = {
    -1.f,  1.f, 0.f, 0.f,
     1.f,  1.f, 1.f, 0.f,
     1.f, -1.f, 1.f, 1.f,

     1.f, -1.f, 1.f, 1.f,
    -1.f, -1.f, 0.f, 1.f,
    -1.f,  1.f, 0.f, 0.f
  };

  glGenBuffers(1, &m_vbo);
  glBindBuffer(GL_ARRAY_BUFFER, m_vbo);
  glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

  const std::string vertSource =R"(
    #version 330
    layout(location=0) in vec2 position;
    layout(location=1) in vec2 coordinate;
    uniform vec2 translation;
    uniform float scale;
    out vec2 Coordinate;
    void main()
    {
       Coordinate = coordinate;
       gl_Position = vec4((position + translation) * scale, 0.0, 1.0);
    }
    )";


  const std::string fragSource =R"(
    #version 330
    in vec2 Coordinate;
    uniform sampler2D tex;
    uniform float gamma;
    layout(location=0) out vec4 outColour;
    uniform int displayMode;
    void main()
    {
      vec4 baseColour=texture(tex,Coordinate);
      switch(displayMode)
      {
        case 0 : outColour=baseColour; break;
        case 1 : outColour=vec4(baseColour.r,0,0,baseColour.a); break; // red
        case 2 : outColour=vec4(0,baseColour.g,0,baseColour.a); break; // green
        case 3 : outColour=vec4(0,0,baseColour.b,baseColour.a); break; // blue
        case 4 : outColour=vec4(baseColour.a,baseColour.a,baseColour.a,1); // alpha are greyscale
        case 5 :
          outColour.rgb = vec3(dot(baseColour.rgb, vec3(0.299, 0.587, 0.114)));
        break;
        }
        outColour.rgb = pow(outColour.rgb, vec3(1.0/gamma));
     }
    )";

  const GLchar* shaderSource=vertSource.c_str();


  auto vertexShader = glCreateShader(GL_VERTEX_SHADER);
  glShaderSource(vertexShader, 1, &shaderSource, NULL);
  glCompileShader(vertexShader);
  printInfoLog(vertexShader);

  shaderSource=fragSource.c_str();
  auto fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
  glShaderSource(fragmentShader, 1, &shaderSource, NULL);
  glCompileShader(fragmentShader);
  printInfoLog(fragmentShader);

  m_shaderProgram = glCreateProgram();
  glAttachShader(m_shaderProgram, vertexShader);
  glAttachShader(m_shaderProgram, fragmentShader);
  glLinkProgram(m_shaderProgram);
  printInfoLog(vertexShader,GL_LINK_STATUS);

  glUseProgram(m_shaderProgram);

  auto attrib = glGetAttribLocation(m_shaderProgram, "position");
  glVertexAttribPointer(attrib, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), 0);
  glEnableVertexAttribArray(attrib);
  attrib = glGetAttribLocation(m_shaderProgram, "coordinate");
  glVertexAttribPointer(attrib, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), (void*)(2 * sizeof(GLfloat)));
  glEnableVertexAttribArray(attrib);

  m_translateUniform = glGetUniformLocation(m_shaderProgram, "translation");
  glUniform2f(m_translateUniform, m_xPos,m_yPos);

  m_scaleUniform = glGetUniformLocation(m_shaderProgram, "scale");
  glUniform1f(m_scaleUniform, m_scale);
  m_modeUniform = glGetUniformLocation(m_shaderProgram, "displayMode");
  glUniform1i(m_modeUniform, 0);

  m_gammaUniform = glGetUniformLocation(m_shaderProgram, "gamma");
  glUniform1f(m_gammaUniform, m_gamma);


  glGenTextures(1, &m_texture);
  glBindTexture(GL_TEXTURE_2D, m_texture);
  glTexImage2D(GL_TEXTURE_2D, 0, m_pixelFormat, m_width, m_height, 0, m_pixelFormat, GL_FLOAT, NULL);

  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
}


void SDLOpenGL::createGLContext()
{
  SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE);
  SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION,4);
  SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION,1);

  SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS,1);
  SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES,4);

  SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE,16);
  SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER,1);

  m_glContext=SDL_GL_CreateContext(m_window);
}



void SDLOpenGL::pollEvent(SDL_Event &_event)
{
  makeCurrent();
  SDL_PollEvent(&_event);
}

void SDLOpenGL::changeScale(float _f)
{
  m_scale=_f;
  glUniform1f(m_scaleUniform, m_scale);
  draw();
}

void SDLOpenGL::reset()
{
  m_scale=1.0f;
  m_xPos=0.0f;
  m_yPos=0.0f;
  glUniform1f(m_scaleUniform, m_scale);
  glUniform2f( m_translateUniform,m_xPos,m_yPos );
  draw();
}

void SDLOpenGL::setPosition(float _x, float _y)
{
  m_xPos=_x;
  m_yPos=_y;
  glUniform2f( m_translateUniform,m_xPos,m_yPos );
  draw();
}

void SDLOpenGL::ErrorExit(const std::string &_msg) const
{
  std::cerr<<_msg<<'\n';
  std::cerr<<SDL_GetError()<<'\n';
  SDL_Quit();
  exit(EXIT_FAILURE);
}

void SDLOpenGL::setRenderMode(RenderMode _m)
{
  switch(static_cast<int>(_m))
  {
    case 0 : glUniform1i(m_modeUniform,0); break;
    case 1 : glUniform1i(m_modeUniform,1); break;
    case 2 : glUniform1i(m_modeUniform,2); break;
    case 3 : glUniform1i(m_modeUniform,3); break;
    case 4 : glUniform1i(m_modeUniform,4); break;
    case 5 : glUniform1i(m_modeUniform,5); break;
  }
}

void SDLOpenGL::setGamma(float _g)
{
  m_gamma=_g;
  glUniform1f(m_gammaUniform,m_gamma);
  draw();
}
