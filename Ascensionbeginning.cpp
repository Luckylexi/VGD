#include "wtypes.h"
#include "SDL.h"
#include <stdio.h>
#include <iostream>
#include <string>

using namespace std;

void GetDesktopResolution(int& horizontal, int& vertical)
{
   RECT desktop;
   // Get a handle to the desktop window
   const HWND hDesktop = GetDesktopWindow();
   // Get the size of screen to the variable desktop
   GetWindowRect(hDesktop, &desktop);
   // The top left corner will have coordinates (0,0)
   // and the bottom right corner will have coordinates
   // (horizontal, vertical)
   horizontal = desktop.right;
   vertical = desktop.bottom;
}

class Game {
	SDL_Window *window;
	SDL_Renderer *renderer;
	public:
		Game(string name){
			int w;
			int h;
			window = NULL;
			renderer = NULL;
			SDL_Init(SDL_INIT_VIDEO);
			GetDesktopResolution(w,h);
			window = SDL_CreateWindow(
				name.c_str(), 
				SDL_WINDOWPOS_UNDEFINED,
				SDL_WINDOWPOS_UNDEFINED,
				w/3,
				h/1.5,
				SDL_WINDOW_OPENGL);
				
			if(window == NULL){
				printf("Could not create window: %s\n", SDL_GetError());
				return;
				}
				
			renderer = SDL_CreateRenderer(window, -1, 0);
			if(renderer == NULL){
				printf("Could not create renderer: %s\n", SDL_GetError());
				return;
				}
			}
			
		SDL_Renderer *getRenderer(){ return renderer;}
		SDL_Window *getWindow() {return window;}
		~Game(){
				SDL_DestroyWindow(window);
				SDL_Quit();
			}
			virtual void init()=0;
			virtual void loop()=0;	  
			void run() {
			if (renderer==NULL || window==NULL) return;
			init();
			loop();
		}
};

class MyGame:public Game{
	SDL_Texture *texture;
	SDL_Rect src,dest;
	public:
	MyGame(): Game("Ascension"){}
	void init() {
		SDL_Surface *background;
		background=SDL_LoadBMP("Graphics/SkyLand.bmp");
		// The window is open: could enter program loop here (see SDL_PollEvent())
		if (background==NULL) {
			printf("Could not load %s : %s/n", SDL_GetError());
			return;
		}
		SDL_Renderer *renderer = getRenderer();
		texture = SDL_CreateTextureFromSurface(renderer, background);
		if (texture == NULL){
			fprintf(stderr, "CreateTextureFromSurface failed: %s\n", SDL_GetError());
			}
		
		SDL_QueryTexture(texture, NULL, NULL, &(src.w), &(src.h));
		src.x = 0;
		src.y = 0;
		dest.w = src.w;
		dest.h = src.h;
		dest.x = 0;
		dest.y = 0;
		SDL_FreeSurface(background);
	}
		void loop() {
  	  for (int x=0;x<480;x++) {
	    dest.x=x;
	    dest.y=x;
	    SDL_Renderer *renderer=getRenderer();
        SDL_RenderCopy(renderer, texture, &src, &dest);
        SDL_RenderPresent(renderer);
        SDL_Delay(16);  // Pause execution for 3000 milliseconds, for example
      }
	}
};

int main(int argc, char* argv[]) {
	Game *g;
	g = new MyGame();
	g->run();
	delete g;
	return 0;
	}
