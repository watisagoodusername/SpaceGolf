#include "include/camera.h"
#include <raylib.h>

camera::camera(Vector2 pos, float sc) {
	position = pos;
	zoom = sc;
}

Vector2 camera::worldtocamspace(Vector2 p) {
	p.x -= position.x;
	p.y -= position.y;

	p.x *= zoom;
	p.y *= zoom;

	p.x += 500;
	p.y += 500;

	return p;
}

Vector2 camera::camtoworldspace(Vector2 p) {
	p.x -= 500;
	p.y -= 500;

	p.x /= zoom;
	p.y /= zoom;

	p.x += position.x;
	p.y += position.y;

	return p;
}

float camera::rescale(float x) {
	x *= zoom;

	return x;
}

void camera::changepos(Vector2 fac) {
	position.x += fac.x / zoom;
	position.y += fac.y / zoom;
}

void camera::changezoom(float fac) {
	zoom *= fac;
}

void camera::set_pos(Vector2 pos) {
	position = pos;
}

void camera::set_zoom(float sc) {
	zoom = sc;
}