#include <raylib.h>
#include <raymath.h>
#include <cmath>
#include <iostream>


bool pincircle(Vector2 ppos, Vector2 cpos, float radius) {// determines if a point is inside a circle
    float xdif = ppos.x - cpos.x;
    float ydif = ppos.y - cpos.y;
    float tdif = sqrt(xdif * xdif + ydif * ydif);//distance between points
    if (tdif < radius) {
        return true;
    }
    
    return false;
}

bool pinrect(Vector2 ppos, Vector2 cpos, Vector2 size) {// determines if a point is inside a rectangle
    float xdif = ppos.x - cpos.x;
    float ydif = ppos.y - cpos.y;
    if (-size.x / 2 < xdif and xdif < size.x / 2 and -size.y / 2 < ydif and ydif < size.y / 2) {
        return true;
    }
    return false;
}

bool rectoverlap(Vector2 pos1, Vector2 pos2, Vector2 size1, Vector2 size2) {// determines if a point is inside a rectangle
    float xdif = pos1.x - pos2.x;
    float ydif = pos1.y - pos2.y;
    if (-(size1.x + size2.x) / 2 < xdif and xdif < (size1.x + size2.x) / 2 and -(size1.y + size2.y) / 2 < ydif and ydif < (size1.y + size2.y) / 2) {
        return true;
    }
    return false;
}

bool circleoverlap(Vector2 pos1, Vector2 pos2, float rad1, float rad2) {
    if (Vector2Distance(pos1, pos2) < rad1 + rad2) {
        return true;
    }
    return false;
}

void resolvecirclecollision(Vector2& pos1, Vector2& pos2, float r1, float r2, float m1, float m2, Vector2 v1, Vector2 v2) {//move circles outside eachother
    float xdif = pos1.x - pos2.x;
    float ydif = pos1.y - pos2.y;

    if (xdif == 0) {
        xdif = 0.001;
    }
    if (ydif == 0) {
        ydif = 0.001;
    }

    float tdif = sqrt(xdif * xdif + ydif * ydif);//distance between points

    xdif /= tdif;
    ydif /= tdif;//normalised

    float rt = r1 + r2;

    float tomovetotal = rt - tdif;

    float tomove1 = (m2 * tomovetotal) / (m1 + m2);
    float tomove2 = (m1 * tomovetotal) / (m1 + m2);

    float relativev = Vector2Length(Vector2Add(v1, v2));

    float posscale = 1;//relativev * 0.05 + 1;

    pos1.x += xdif * tomove1 * posscale;
    pos1.y += ydif * tomove1 * posscale;
    pos2.x -= xdif * tomove2 * posscale;
    pos2.y -= ydif * tomove2 * posscale;
}

void resolverectcollision(Vector2& pos1, Vector2& pos2, Vector2 s1, Vector2 s2, float m1, float m2, Vector2 v1, Vector2 v2) {
    Vector2 dif = Vector2{ pos1.x - pos2.x, pos1.y - pos2.y };// distance between centers

    float xoverlap = (s1.x + s2.x) / 2 - abs(dif.x);
    float yoverlap = (s1.y + s2.y) / 2 - abs(dif.y);

    Vector2 sendoutsidev1 = Vector2Zero();
    Vector2 sendoutsidev2 = Vector2Zero();// find the distance required to send the rects outside each other

    if (xoverlap <= yoverlap) {// find velocity to send them outside if a suitable solution based on velocity is not found
        sendoutsidev1 = Vector2{ ((0 < dif.x) - (dif.x < 0)) * (m2 * xoverlap) / (m1 + m2), 0 };
        sendoutsidev2 = Vector2{ ((0 < dif.x) - (dif.x < 0)) * (m1 * -xoverlap) / (m1 + m2), 0 };
    }
    else {
        sendoutsidev1 = Vector2{ 0, ((0 < dif.y) - (dif.y < 0)) * (m2 * yoverlap) / (m1 + m2) };
        sendoutsidev2 = Vector2{ 0, ((0 < dif.y) - (dif.y < 0)) * (m1 * -yoverlap) / (m1 + m2) };
    }

    float relativev = Vector2Length(Vector2Add(v1, v2));

    float posscale = relativev * 0.05 + 1;

    pos1.x += sendoutsidev1.x * posscale;
    pos1.y += sendoutsidev1.y * posscale;
    pos2.x += sendoutsidev2.x * posscale;
    pos2.y += sendoutsidev2.y * posscale;
}

void bounce1D(float& vel1, float& vel2, float m1, float m2, float restitution) {
    float v1 = (restitution * m2 * (vel2 - vel1) + m1 * vel1 + m2 * vel2) / (m1 + m2);
    float v2 = (restitution * m1 * (vel1 - vel2) + m2 * vel2 + m1 * vel1) / (m2 + m1);//final velocity calculations for 1D inelastic collisions

    vel1 = v1;
    vel2 = v2;
}

void bounce2D(Vector2& vel1, Vector2& vel2, float m1, float m2, float angle, float restitution) {
    Vector2 rotatedv1 = Vector2Rotate(vel1, angle);
    Vector2 rotatedv2 = Vector2Rotate(vel2, angle);//rotates points so x axis is normal to make calculations easier

    bounce1D(rotatedv1.y, rotatedv2.y, m1, m2, restitution);

    vel1 = Vector2Rotate(rotatedv1, -angle);
    vel2 = Vector2Rotate(rotatedv2, -angle);//return updated velocities
}

void wallbounce(int lowx, int highx, int lowy, int highy, Vector2& pos, Vector2& vel, float xdistance, float ydistance, bool& g) {
    //takes an object size xdistance by ydistance and reflects velocity if outside x/y bounds

    float res = 0.95;

    if (pos.x > highx - xdistance) {
        float overlap = highx - xdistance;
        vel.x = -abs(vel.x * res);
        pos.x = highx - xdistance;
    }
    else if (pos.x < lowx + xdistance) {
        float overlap = lowx + xdistance;
        vel.x = abs(vel.x * res);
        pos.x = lowx + xdistance;
    }
    if (pos.y > highy - ydistance) {
        float overlap = highy - ydistance;
        vel.y = -abs(vel.y * res);
        pos.y = highy - ydistance;
    }
    else if (pos.y < lowy + ydistance) {
        float overlap = lowy + ydistance;
        vel.y = abs(vel.y * res);
        pos.y = lowy + ydistance;
    }
}

