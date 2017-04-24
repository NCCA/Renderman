#ifndef SDLOPENGL_H_
#define SDLOPENGL_H_
#include <SDL.h>
#include <string>
#ifdef __APPLE__
  #include <unistd.h>
//  #include <OpenGL/gl.h>
#include <OpenGL/gl3.h>
#elif __linux__

  #include <GL/glew.h>
  #include <GL/gl.h>
#endif
class SDLOpenGL
{
  public :
    SDLOpenGL(const std::string &_name, int _x, int _y, int _width, int _height);

    void makeCurrent() { SDL_GL_MakeCurrent(m_window,m_glContext);}
    void swapWindow() { SDL_GL_SwapWindow(m_window); }

    void pollEvent(SDL_Event &_event);
    void createSurface();
    void updateImage(const float* _image);
    void draw();
  private :
    /// @brief width of screen
    int m_width;
    /// @brief height of screen
    int m_height;
    // xpos of window
    int m_x;
    // ypos of window
    int m_y;
    // name of window
    std::string m_name;
    GLuint m_texture;
    GLuint m_shader_program;
    GLuint m_vertex_shader;
    GLuint m_fragment_shader;
    GLuint m_vbo;
    GLuint m_vao;
    GLint m_pos_attrib;
    GLint m_tex_attrib;
    GLint m_trans_uniform;
    GLint m_scale_uniform;
    void init();

    SDL_GLContext m_glContext;
    void createGLContext();

    void ErrorExit(const std::string &_msg) const;

    SDL_Window *m_window;

};

#endif
