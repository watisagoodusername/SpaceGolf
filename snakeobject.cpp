#include "include/snakeobject.h"

snakeobject::snakeobject(float xpos, float ypos, int xvel, int yvel) {
	position.x = xpos;
	position.y = ypos;
	velocity.x = (float)xvel;
	velocity.y = (float)yvel;
}

void snakeobject::update(bool w, bool a, bool s, bool d) {
	if (velocity.x == 0) {
		if (w) {
			velocity.y = 1;
			velocity.x = 0;
		}
		else if (s) {
			velocity.y = -1;
			velocity.x = 0;
		}
	}
	else if (velocity.y == 0) {
		if (d) {
			velocity.y = 0;
			velocity.x = 1;
		}
		else if (a) {
			velocity.y = 0;
			velocity.x = -1;
		}
	}

	position.x += velocity.x * 5;
	position.y += velocity.y * 5;
}