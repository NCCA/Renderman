#include "ndspy.h"
#include <SDL.h>
#include <limits>
#include "SDLOpenGL.h"
#include <memory>
#ifdef __cplusplus
extern "C" {
#endif


//SDL_Window *window;
//SDL_Renderer *renderer;
//SDL_Texture* texture;
static std::vector< float > g_pixels;
static size_t g_width,g_height;
static std::unique_ptr<SDLOpenGL> window;
/*
void SDLErrorExit(const std::string &_msg)
{
  std::cerr<<_msg<<"\n";
  std::cerr<<SDL_GetError()<<"\n";
  SDL_Quit();
  exit(EXIT_FAILURE);
}
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
   int channels;
   int width, height;
} *MyImageType;

PRMANEXPORT PtDspyError DspyImageOpen(
              PtDspyImageHandle *pvImage,
              const char *drivername,
              const char *filename,
              int width,
              int height,
              int paramCount,
              const UserParameter *parameters,
              int formatCount,
              PtDspyDevFormat *format,
              PtFlagStuff *flagstuff)
{
  PtDspyError ret;
  MyImageType image;
    std::cerr<<"started driver\n";
    std::cerr<<"width "<<width<<' '<<"height "<<height<<'\n';
   /* We want to receive the pixels one after the other */

  // flagstuff->flags |= PkDspyBucketOrderHorizontal;//   PkDspyFlagsWantsScanLineOrder;
   flagstuff->flags |= PkDspyBucketOrderRandom;
   /* Do stupidity checking */

   if (0 == width) width = 640;
   if (0 == height) height = 480;

   image = NULL;
   ret = PkDspyErrorNone;

   image = (MyImageType) malloc(sizeof(*image));

//   startSDL(width,height);
   g_pixels.resize(width*height*4,0);
   window.reset( new SDLOpenGL("SDL Prman",0,0,width,height));
  // window->createSurface();
   if (NULL != image)
   {
      int i;

      image->channels = formatCount;
      image->width = width;
      image->height = height;

   }
   *pvImage = image;
   return ret;
}

PRMANEXPORT PtDspyError DspyImageQuery(PtDspyImageHandle pvImage,
     PtDspyQueryType querytype,
     int datalen,
     void *data)
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
            std::cerr<<"write Query\n";

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
                  if (0 == image->width ||
                      0 == image->height)
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
          case PkRenderingStartQuery :
          {
              PtDspyRenderingStartQuery startLocation;
              std::cerr<<"Start rendering\n";
              if (datalen > sizeof(startLocation))
                  datalen = sizeof(startLocation);

              if (image) {
                  /*
                   * initialize values in startLocation
                   */
                  memcpy(data, &startLocation, datalen);
              } else {
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

PRMANEXPORT PtDspyError DspyImageData(PtDspyImageHandle pvimage,
    int xmin,
    int xmax,
    int ymin,
    int ymax,
    int entrysize,
    const unsigned char *data
   )
{

  PtDspyError ret=PkDspyErrorNone;
  int oldx;
  oldx = xmin;
    std::cerr<<"entry size" << entrysize<<'\n';
    for (;ymin < ymax; ++ymin)
    {      
       for (xmin = oldx; xmin < xmax; ++xmin)
       {
        const float *ptr = reinterpret_cast<const float*> (data);
        size_t offset = ( g_width * 4 * ymin ) + xmin * 4;
        std::cerr<<"offset "<<offset<<' '<<ptr[3]<<' '<<ptr[2]<<' '<<ptr[1]<<' '<<ptr[0]<<'\n';
        g_pixels[ offset + 0 ]=ptr[3];
        g_pixels[ offset + 1 ]=ptr[2];
        g_pixels[ offset + 2 ]=ptr[1];
        g_pixels[ offset + 3 ] = ptr[0];
        data += entrysize;

       }
       window->updateImage(&g_pixels[0]);
       window->draw();
    }

//    SDL_UpdateTexture (texture, 0,&pixels[0],  g_width * 4 );

//    SDL_RenderCopy( renderer, texture, NULL, NULL );
//    SDL_RenderPresent( renderer );
     SDL_Event event;
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

             default : break;
           } // end of key process
         } // end of keydown

       } // end of event switch
    return ret;
}

PRMANEXPORT PtDspyError DspyImageClose(PtDspyImageHandle pvImage)
{
  std::cerr<<"close\n";
  PtDspyError ret;

  // sdl event processing data structure
  SDL_Event event;
  bool quit=false;
  while(quit !=true)
  {
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
          case SDLK_ESCAPE : quit=true;  break;

          default : break;
        } // end of key process
      } // end of keydown

      default : break;
    } // end of event switch
    window->draw();
  }// end of quit


  MyImageType image = (MyImageType )pvImage;
  free(image);
  ret = PkDspyErrorNone;
  return ret;
}

#ifdef __cplusplus
}
#endif
