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

  const GLchar* vertex_source =
    "#version 330\n"
    "in vec2 position;"
    "in vec2 coordinate;"
    "uniform vec2 translation;"
    "uniform float scale;"
    "out vec2 Coordinate;"
    "void main()"
    "{"
    "   Coordinate = coordinate;"
    "   gl_Position = vec4((position + translation) * scale, 0.0, 1.0);"
    "}";

  const GLchar* fragment_source =
    "#version 330\n"
    "in vec2 Coordinate;"
    "uniform sampler2D tex;"
    "out vec4 outColor;"
    "void main()"
    "{"
    "   outColor = texture(tex, Coordinate);"
    "}";

  m_vertex_shader = glCreateShader(GL_VERTEX_SHADER);
  glShaderSource(m_vertex_shader, 1, &vertex_source, NULL);
  glCompileShader(m_vertex_shader);
  printInfoLog(m_vertex_shader);

  m_fragment_shader = glCreateShader(GL_FRAGMENT_SHADER);
  glShaderSource(m_fragment_shader, 1, &fragment_source, NULL);
  glCompileShader(m_fragment_shader);
  printInfoLog(m_fragment_shader);

  m_shader_program = glCreateProgram();
  glAttachShader(m_shader_program, m_vertex_shader);
  glAttachShader(m_shader_program, m_fragment_shader);
  glLinkProgram(m_shader_program);
  printInfoLog(m_vertex_shader,GL_LINK_STATUS);

  glUseProgram(m_shader_program);

  m_pos_attrib = glGetAttribLocation(m_shader_program, "position");
  glVertexAttribPointer(m_pos_attrib, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), 0);
  glEnableVertexAttribArray(m_pos_attrib);
  std::cerr<<"Pos "<<m_pos_attrib<<'\n';
  m_tex_attrib = glGetAttribLocation(m_shader_program, "coordinate");
  glVertexAttribPointer(m_tex_attrib, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), (void*)(2 * sizeof(GLfloat)));
  glEnableVertexAttribArray(m_tex_attrib);
  std::cerr<<"tex "<<m_tex_attrib<<'\n';

  m_trans_uniform = glGetUniformLocation(m_shader_program, "translation");
  glUniform2f(m_trans_uniform, m_xPos,m_yPos);
  std::cerr<<"trans "<<m_trans_uniform<<'\n';

  m_scale_uniform = glGetUniformLocation(m_shader_program, "scale");
  glUniform1f(m_scale_uniform, m_scale);
  std::cerr<<"scale "<<m_scale_uniform<<'\n';

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
  glUniform1f(m_scale_uniform, m_scale);
  draw();
}

void SDLOpenGL::reset()
{
  m_scale=1.0f;
  m_xPos=0.0f;
  m_yPos=0.0f;
  glUniform1f(m_scale_uniform, m_scale);
  glUniform2f( m_trans_uniform,m_xPos,m_yPos );
  draw();
}

void SDLOpenGL::setPosition(float _x, float _y)
{
  m_xPos=_x;
  m_yPos=_y;
  glUniform2f( m_trans_uniform,m_xPos,m_yPos );
  draw();
}

void SDLOpenGL::ErrorExit(const std::string &_msg) const
{
  std::cerr<<_msg<<'\n';
  std::cerr<<SDL_GetError()<<'\n';
  SDL_Quit();
  exit(EXIT_FAILURE);
}
