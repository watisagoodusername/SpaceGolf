#include "include/rectcollide.h"
#include "include/rigidbody.h"
#include "include/PhysicsFunctions.h"
#include "raylib.h"
#include <iostream>
#include "include/camera.h"

rectcollide::rectcollide(float xsize, float ysize, float xpos, float ypos, float m, float xvel, float yvel) {
    size.x = xsize;
    size.y = ysize;
    mass = xsize * ysize * m;
    position.x = xpos;
    position.y = ypos;
    velocity.x = xvel;
    velocity.y = yvel;
    maxspeed = 50;
}

void rectcollide::rectballcollision(ballcollide* compare) {
    Vector2 p1 = position;
    Vector2 p2 = compare->get_pos();// position values

    Vector2 s1 = size;
    float r2 = compare->get_r();

    Vector2 dif = Vector2{ p1.x - p2.x, p1.y - p2.y };// distance between centers
    
    //if (s1.x / 2 + r2 > dif.x and -s1.x / 2 - r2 < dif.x and s1.y / 2 > dif.y and -s1.y / 2 < dif.y or s1.x / 2 > dif.x and -s1.x / 2 < dif.x and s1.y / 2 + r2 > dif.y and -s1.y / 2 - r2 < dif.y) {
    if (s1.x / 2 + r2 > dif.x and -s1.x / 2 + r2 < dif.x and s1.y / 2 + r2 > dif.y and -s1.y / 2 + r2 < dif.y) {
        //when collision occures with the edge of the rect
       
        Vector2 v1 = velocity;
        Vector2 v2 = compare->get_vel(); //velocity values, passed by value

        float m1 = mass;
        float m2 = compare->get_m();// mass

        float xoverlap, yoverlap;

        xoverlap = (s1.x + 2 * r2) / 2 - abs(dif.x);
        yoverlap = (s1.y + 2 * r2) / 2 - abs(dif.y); // how far the squares overlapped, multiplied by the sign of dif

        // make sure both velocities arent 0 to avoid division by 0 errors

        if (v1.x != 0 or v1.y != 0 or v2.x != 0 or v2.y != 0) {
            // if there is a relative velocity assume that they are inside eachother due to velocity 
            //and send them outside by reversing velocity until they are no longer overlapping

            float xscalefac;
            float yscalefac;//how much of a frame they have been overlapping for

            xscalefac = xoverlap / abs(v2.x - v1.x);
            yscalefac = yoverlap / abs(v2.y - v1.y);// one of these will always be between 0 and 1 in a standard collision 
            //whichever one of these variables is smaller is the axis of the collision

            if (xscalefac > 1) {
                xscalefac = 1;
            }
            if (yscalefac > 1) {
                yscalefac = 1;
            }// limits them to 1 to stop funny business ( sort of )

            if (xscalefac < yscalefac) {//finding the distance to move to send the objects to the moment of collision
                // if x has a lower scalefac that means the collision was on the x axis 
                //putting any position changes here breaks things
                bounce1D(v1.x, v2.x, m1, m2, 0.95);
            }
            else {
                bounce1D(v1.y, v2.y, m1, m2, 0.95);
            }
        }
        velocity = v1;
        compare->set_vel(v2);//applies changes
    }
    else {
        int t = 0;
        int corner = -1; 
        while (t < 4) {
            if (pincircle(get_corner(t), p2, r2)) {
                corner = t;
                t = 4;
            }
            t++;
        }
        if (corner >= 0) {

            Vector2 c = get_corner(corner);
            Vector2 dif = Vector2Subtract(c, p2);// distance between circles

            float angle = atan2(dif.x, dif.y);

            Vector2 v1 = velocity;
            Vector2 v2 = compare->get_vel(); //velocity values, passed by value

            float m1 = mass;
            float m2 = compare->get_m();// mass

            bounce2D(v1, v2, m1, m2, angle, 0.95);//velocity calculations

            velocity = v1;
            compare->set_vel(v2);//applies velocity
        }
    }

}

void rectcollide::rectballposition(ballcollide* compare) {
    Vector2 p1 = position;
    Vector2 p2 = compare->get_pos();// position values

    Vector2 s1 = size;
    float r2 = compare->get_r();

    Vector2 v1 = velocity;
    Vector2 v2 = compare->get_vel(); //velocity values, passed by value

    Vector2 dif = Vector2{ p1.x - p2.x, p1.y - p2.y };// distance between centers

    //if (s1.x / 2 + r2 > dif.x and -s1.x / 2 - r2 < dif.x and s1.y / 2 > dif.y and -s1.y / 2 < dif.y or s1.x / 2 > dif.x and -s1.x / 2 < dif.x and s1.y / 2 + r2 > dif.y and -s1.y / 2 - r2 < dif.y) {
    if (s1.x/2 + r2 > dif.x and -s1.x / 2 + r2 < dif.x and s1.y / 2 + r2 > dif.y and -s1.y / 2 + r2 < dif.y) {
        float m1 = mass;
        float m2 = compare->get_m();// mass

        float xoverlap = (s1.x + 2 * r2) / 2 - abs(dif.x);
        float yoverlap = (s1.y + 2 * r2) / 2 - abs(dif.y);

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

        p1.x += sendoutsidev1.x * posscale;
        p1.y += sendoutsidev1.y * posscale;
        p2.x += sendoutsidev2.x * posscale;
        p2.y += sendoutsidev2.y * posscale;

    }
    else {
        int t = 0;
        int corner = -1;
        while (t < 4) {
            if (pincircle(get_corner(t), p2, r2)) {
                corner = t;
                t = 4;
            }
            t++;
        }
        if (corner >= 0) {

            Vector2 c = get_corner(corner);
            Vector2 dif = Vector2Subtract(c, p2);// distance between circles

            float angle = atan2(dif.x, dif.y);

            Vector2 v1 = velocity;
            Vector2 v2 = compare->get_vel(); //velocity values, passed by value

            float m1 = mass;
            float m2 = compare->get_m();// mass

            resolvecirclecollision(c, p2, 0, r2, m1, m2, v1, v2);//changes p1 and p2 so they arent inside each other

            p1 = posfromcorner(c, corner);
        }
    }

    set_pos(p1);
    compare->set_pos(p2);//applies position
}

void rectcollide::rectcollision(rectcollide* compare) {
    Vector2 p1 = position;
    Vector2 p2 = compare->get_pos();// position values

    Vector2 s1 = size;
    Vector2 s2 = compare->get_size();

    if (rectoverlap(p1, p2, s1, s2)) {
        //when collision occures
        Vector2 dif = Vector2{ p1.x - p2.x, p1.y - p2.y};// distance between centers

        Vector2 v1 = velocity;
        Vector2 v2 = compare->get_vel(); //velocity values, passed by value

        float m1 = mass;
        float m2 = compare->get_m();// mass

        float xoverlap, yoverlap;

        xoverlap = (s1.x + s2.x) / 2 - abs(dif.x);
        yoverlap = (s1.y + s2.y) / 2 - abs(dif.y); // how far the squares overlapped, multiplied by the sign of dif

        // make sure both velocities arent 0 to avoid division by 0 errors

        // finding which side overlapped first

        if (v1.x != 0 or v1.y != 0 or v2.x != 0 or v2.y != 0) {
            // if there is a relative velocity assume that they are inside eachother due to velocity 
            //and send them outside by reversing velocity until they are no longer overlapping

            float xscalefac;
            float yscalefac;//how much of a frame they have been overlapping for

            xscalefac = xoverlap / abs(v2.x - v1.x);
            yscalefac = yoverlap / abs(v2.y - v1.y);// one of these will always be between 0 and 1 in a standard collision 
            //whichever one of these variables is smaller is the axis of the collision

            if (xscalefac > 1) {
                xscalefac = 1;
            }
            if (yscalefac > 1) {
                yscalefac = 1;
            }// limits them to 1 to stop funny business ( sort of )
            
            if (xscalefac < yscalefac) {//finding the distance to move to send the objects to the moment of collision
                // if x has a lower scalefac that means the collision was on the x axis 
                //putting any position changes here breaks things
                bounce1D(v1.x, v2.x, m1, m2, 0.95);
            }
            else {
                bounce1D(v1.y, v2.y, m1, m2, 0.95);
            }
        }

        velocity = v1;
        compare->set_vel(v2);//applies changes
    }
    
}

void rectcollide::rectposition(rectcollide* compare) {
    Vector2 p1 = position;
    Vector2 p2 = compare->get_pos();// position values

    Vector2 s1 = size;
    Vector2 s2 = compare->get_size();

    Vector2 v1 = velocity;
    Vector2 v2 = compare->get_vel(); //velocity values, passed by value

    if (rectoverlap(p1, p2, s1, s2)) {

        float m1 = mass;
        float m2 = compare->get_m();// mass

        resolverectcollision(p1, p2, s1, s2, m1, m2, v1, v2);

    }
    set_pos(p1);
    compare->set_pos(p2);//applies position
}

void rectcollide::walls() {
    wallbounce(0, 1000, 0, 1000, position, velocity, size.x / 2, size.y / 2, grounded);
}

void rectcollide::update(Vector2 gravity, Vector2 mousepos, bool pressed, bool released) {
    if (pinrect(mousepos, position, size) && !held && pressed) {
        held = true;
    }
    if (held && released) {
        held = false;
        velocity = Vector2ClampValue(velocity, 0, maxspeed);
    }

    rigidbody::update(gravity, mousepos);
}

void rectcollide::draw(camera cam) {
    Vector2 pos = cam.worldtocamspace(position);
    float xsize = cam.rescale(size.x);
    float ysize = cam.rescale(size.y);

    DrawRectangle(pos.x - xsize / 2, pos.y - ysize / 2, xsize, ysize, BLACK);
    DrawRectangle(pos.x - xsize / 2 + 5, pos.y - ysize / 2 + 5, xsize - 10, ysize - 10, DARKBLUE);
}

Vector2 rectcollide::get_corner(int num) {//0 = top left, 1 = top right, 2 = bottom left, 3 = bottom right
    Vector2 cornerpos;
    if (num == 0) {
        cornerpos.x = position.x - size.x / 2;
        cornerpos.y = position.y - size.y / 2;
    }
    else if (num == 1) {
        cornerpos.x = position.x + size.x / 2;
        cornerpos.y = position.y - size.y / 2;
    }
    else if (num == 2) {
        cornerpos.x = position.x - size.x / 2;
        cornerpos.y = position.y + size.y / 2;
    }
    else if (num == 3) {
        cornerpos.x = position.x + size.x / 2;
        cornerpos.y = position.y + size.y / 2;
    }
    else {
        cornerpos = Vector2{ 0, 0 };
    }
    return cornerpos;
}

Vector2 rectcollide::posfromcorner(Vector2 c, int num) {//0 = top left, 1 = top right, 2 = bottom left, 3 = bottom right
    Vector2 cornerpos;
    if (num == 3) {
        cornerpos.x = c.x - size.x / 2;
        cornerpos.y = c.y - size.y / 2;
    }
    else if (num == 2) {
        cornerpos.x = c.x + size.x / 2;
        cornerpos.y = c.y - size.y / 2;
    }
    else if (num == 1) {
        cornerpos.x = c.x - size.x / 2;
        cornerpos.y = c.y + size.y / 2;
    }
    else if (num == 0) {
        cornerpos.x = c.x + size.x / 2;
        cornerpos.y = c.y + size.y / 2;
    }
    else {
        cornerpos = Vector2{ 0, 0 };
    }
    return cornerpos;
}

void rectcollide::set_vel(Vector2 v) {
    velocity = v;
}