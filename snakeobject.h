#pragma once
#include <raylib.h>

class snakeobject
{
	Vector2 velocity;
	Vector2 position;
public:
	snakeobject(float xpos, float ypos, int xvel, int yvel);
	~snakeobject() {}

	void update(bool w, bool a, bool s, bool d);

	Vector2 get_position() { return position; }
};

