#pragma once
#include "include/rigidbody.h"
#include "include/PhysicsFunctions.h"
#include <raylib.h>
#include <iostream>

rigidbody::rigidbody() {
    mass = 0;
    position = Vector2{ 0, 0 };
    velocity = Vector2{ 0, 0 };
    changeposition = Vector2{ 0, 0 };
    changevelocity = Vector2{ 0, 0 };
    maxspeed = 50;
}

void rigidbody::clicked(Vector2 mousepos, float maxspeed) {
    Vector2 dif = Vector2Subtract(mousepos, position);
    velocity = dif;
    //position = Vector2Subtract(mousepos, dif);
}

void rigidbody::update(Vector2 gravity, Vector2 mousepos) {
    if (held) {
        clicked(mousepos,maxspeed);
    }

    if (!grounded) {
        velocity.x += gravity.x;
        velocity.y += gravity.y;
    }

    position = Vector2Add(position, velocity);
    //position = Vector2Add(position, changeposition);
    changeposition = Vector2Zero();
    
    grounded = false;
}

void applychanges() {

}

void rigidbody::set_vel(Vector2 v) {
    velocity = v;
}
void rigidbody::set_pos(Vector2 p) {
    //changeposition = Vector2Subtract(p, position);
    position = p;
}