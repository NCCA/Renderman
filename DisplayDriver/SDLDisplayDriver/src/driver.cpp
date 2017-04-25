#include "ndspy.h"
#include <SDL.h>
#include <limits>
#include "SDLOpenGL.h"
#include <memory>
#include <chrono>

#ifdef __cplusplus
extern "C" {
#endif

static std::vector< float > g_pixels;
static size_t g_width,g_height;
static std::unique_ptr<SDLOpenGL> window;
static std::chrono::time_point<std::chrono::system_clock> g_start, g_end;
static float g_xPos=0.0f;
static float g_yPos=0.0f;
PtDspyError processEvents();
typedef struct
{
   int channels;
   int width, height;
} *MyImageType;

PRMANEXPORT PtDspyError DspyImageOpen(PtDspyImageHandle *pvImage,
              const char *,const char *filename,
              int width,int height,
              int ,const UserParameter *,
              int formatCount,PtDspyDevFormat *, PtFlagStuff *flagstuff)
{
  PtDspyError ret;
  MyImageType image;
  std::cerr<<"started driver\n";
  std::cerr<<"width "<<width<<' '<<"height "<<height<<'\n';
  flagstuff->flags |= PkDspyBucketOrderSpaceFill;
  flagstuff->flags |= PkDspyFlagsWantsNullEmptyBuckets;
  /* Do stupidity checking */

  if (0 == width) width = 640;
  if (0 == height) height = 480;

  image = NULL;
  ret = PkDspyErrorNone;

  image = (MyImageType) malloc(sizeof(*image));

  if (NULL != image)
  {
    image->channels = formatCount;
    image->width = width;
    image->height = height;

  }
  *pvImage = image;

  g_pixels.resize(width*height*image->channels,0.4f);
  std::string name="SDL PRMDisplay ";
  name+=filename;
  window.reset( new SDLOpenGL(name.c_str(),0,0,width,height,image->channels));
  g_width=width;
  g_height=height;
  g_start = std::chrono::system_clock::now();

  return ret;
}

PRMANEXPORT PtDspyError DspyImageQuery(PtDspyImageHandle pvImage,
     PtDspyQueryType querytype, int datalen,void *data)
{
  PtDspyError ret;
  MyImageType image = (MyImageType )pvImage;

    ret = PkDspyErrorNone;

    if (datalen > 0 && NULL != data)
    {
      switch (querytype)
      {
          case PkOverwriteQuery:
          {
            PtDspyOverwriteInfo overwriteInfo;
            if (datalen > sizeof(overwriteInfo))
                datalen = sizeof(overwriteInfo);
            overwriteInfo.overwrite = 1;
            overwriteInfo.interactive = 0;
            memcpy(data, &overwriteInfo, datalen);
            break;
          }
          case PkSizeQuery :
          {
            PtDspySizeInfo sizeInfo;
            std::cerr<<"size query "<<image->width<<' '<<image->height<<'\n';
            if (datalen > sizeof(sizeInfo)) {
                datalen = sizeof(sizeInfo);
            }
            if (image)
            {
              if (0 == image->width || 0 == image->height)
              {
                image->width = 640;
                image->height = 480;
              }
              sizeInfo.width = image->width;
              sizeInfo.height = image->height;
              sizeInfo.aspectRatio = 1.0f;

            }
            else
            {
              sizeInfo.width = 640;
              sizeInfo.height = 480;
              sizeInfo.aspectRatio = 1.0f;
            }
            memcpy(data, &sizeInfo, datalen);
            break;
          }

          case PkRedrawQuery :
            PtDspyRedrawInfo overwriteInfo;

            if (datalen > sizeof(overwriteInfo))
                datalen = sizeof(overwriteInfo);
            overwriteInfo.redraw = 0;

            memcpy(data, &overwriteInfo, datalen);

          break;

          case PkRenderingStartQuery :
          {
              PtDspyRenderingStartQuery startLocation;
              std::cerr<<"Start rendering\n";
              if (datalen > sizeof(startLocation))
                  datalen = sizeof(startLocation);

              if (image)
              {
                  memcpy(data, &startLocation, datalen);
              }
              else
              {
                  ret = PkDspyErrorUndefined;
              }
              break;
          }

          default :
              ret = PkDspyErrorUnsupported;
              break;
      }
    }
    else
    {
      ret = PkDspyErrorBadParams;
    }
    return ret;
}

PRMANEXPORT PtDspyError DspyImageData(PtDspyImageHandle pvimage,int xmin,int xmax,int ymin,int ymax,int entrysize,const unsigned char *data)
{
  MyImageType image = (MyImageType )pvimage;

  int oldx;
  oldx = xmin;

  for (;ymin < ymax; ++ymin)
  {
     for (xmin = oldx; xmin < xmax; ++xmin)
     {
      const float *ptr = reinterpret_cast<const float*> (data);
      size_t offset =  g_width * image->channels * ymin  + xmin * image->channels;
      if(image->channels == 4)
      {
        g_pixels[ offset + 0 ]=ptr[1];
        g_pixels[ offset + 1 ]=ptr[2];
        g_pixels[ offset + 2 ]=ptr[3];
        g_pixels[ offset + 3 ]=ptr[0];
      }
      else
      {
        g_pixels[ offset + 0 ]=ptr[0];
        g_pixels[ offset + 1 ]=ptr[1];
        g_pixels[ offset + 2 ]=ptr[2];
      }
      data += entrysize;

     }
  }

  window->updateImage(&g_pixels[0]);

  window->draw();
  return processEvents();
}

PRMANEXPORT PtDspyError DspyImageClose(PtDspyImageHandle pvImage)
{
  std::cerr<<"close\n";
  PtDspyError ret;
  g_end = std::chrono::system_clock::now();

 std::chrono::duration<double> elapsed_seconds = g_end-g_start;
 std::time_t end_time = std::chrono::system_clock::to_time_t(g_end);

 std::cout << "finished computation at " << std::ctime(&end_time)
           << "elapsed time: " << elapsed_seconds.count() << "s\n";
// sdl event processing data structure
  PtDspyError quit=PkDspyErrorNone;
  while(quit !=PkDspyErrorCancel)
  {
    quit=processEvents();
    window->draw();
  }// end of quit


  MyImageType image = (MyImageType )pvImage;
  free(image);
  ret = PkDspyErrorNone;
  return ret;
}


PtDspyError processEvents()
{
  SDL_Event event;
  PtDspyError ret = PkDspyErrorNone;

  window->pollEvent(event);

    switch (event.type)
    {
      // this is the window x being clicked.

      // now we look for a keydown event
      case SDL_KEYDOWN:
      {
        switch( event.key.keysym.sym )
        {
          // if it's the escape key quit
        case SDLK_ESCAPE : ret=PkDspyErrorCancel;  break;
        case SDLK_EQUALS :
        case SDLK_PLUS :
         window->changeScale( window->scale()+0.1f);

        break;
        case SDLK_MINUS :
          window->changeScale( window->scale()-0.1f);
         break;
        case SDLK_UP :
          g_yPos+=0.1;
          window->setPosition(g_xPos,g_yPos);
         break;
        case SDLK_DOWN :
          g_yPos-=0.1;
          window->setPosition(g_xPos,g_yPos);
         break;

        case SDLK_LEFT :
          g_xPos-=0.1;
          window->setPosition(g_xPos,g_yPos);
         break;
        case SDLK_RIGHT :
          g_xPos+=0.1;
          window->setPosition(g_xPos,g_yPos);
         break;

      case SDLK_SPACE :
          g_xPos=0.0f;
          g_yPos=0.0f;
        window->reset();

       break;

        case SDLK_1 : window->setRenderMode(SDLOpenGL::RenderMode::ALL); break;
        case SDLK_2 : window->setRenderMode(SDLOpenGL::RenderMode::RED); break;
        case SDLK_3 : window->setRenderMode(SDLOpenGL::RenderMode::GREEN); break;
        case SDLK_4 : window->setRenderMode(SDLOpenGL::RenderMode::BLUE); break;
        case SDLK_5 : window->setRenderMode(SDLOpenGL::RenderMode::ALPHA); break;
        case SDLK_6 : window->setRenderMode(SDLOpenGL::RenderMode::GREY); break;
        case SDLK_LEFTBRACKET : window->setGamma(window->gamma()-0.1f); break;
        case SDLK_RIGHTBRACKET : window->setGamma(window->gamma()+0.1f); break;

        default : break;
        } // end of key process
      } // end of keydown
    } // end of event switch
  return ret;
}


#ifdef __cplusplus
}
#endif
