#include <iostream>
#include <raylib.h>
#include <vector>
#include "include/PhysicsFunctions.h"
#include "include/rigidbody.h"
#include "include/ballcollide.h"
#include "include/rectcollide.h"
#include "include/createobject.h"
#include "include/camera.h"
#include "include/snakeobject.h"
#include "slider2d.h"

int main() {

    bool updatefirst = true;

    int followedball = -1; 

    int screenwidth = 1000;
    int screenheight = 1000;
    InitWindow(screenwidth, screenheight, "physics");

    SetTargetFPS(60);

    createobject ct("ball");

    camera cam(Vector2 {500, 500}, 1);

    std::vector<ballcollide> balls = { ballcollide(20, 50, 50, 1, 5, 4) };
    std::vector<rectcollide> boxes = { rectcollide(20, 20, 500, 500, 1, -2, 3) };
    balls.shrink_to_fit();
    boxes.shrink_to_fit();
    int ballcount = balls.size();
    int boxcount = boxes.size();

    Vector2 gravity = Vector2{ 0, 0.5 };
    slider2d gravcontrol(30, 30, 100, 100, -1, 1, -1, 1, 0, 0.5);

    Image wizardimg = LoadImage("Resources/Wizardofphysics.png"); // Loaded in CPU memory (RAM)
    Image wizardimg2 = LoadImage("Resources/Wizardofphysics.png");

    ImageResizeNN(&wizardimg, 160, 160);
    ImageResize(&wizardimg2, 170, 170);

    Texture2D wizard = LoadTextureFromImage(wizardimg);// Image converted to texture, GPU memory (VRAM)
    Texture2D wizardshadow = LoadTextureFromImage(wizardimg2);

    UnloadImage(wizardimg);
    UnloadImage(wizardimg2);

    bool game = true;
    while (game)
    {
        float dt = GetFrameTime();
        int fps = GetFPS();

        if (WindowShouldClose()) {
            game = false;
        }

        Vector2 mousepos = cam.camtoworldspace(GetMousePosition());

        bool mousedown = false;
        if (IsMouseButtonDown(0)) {
            mousedown = true;
        }
        if (IsMouseButtonPressed(1)) {
            if (!ct.active) {
                ct.initcreation(mousepos);
            }
        }
        if (IsMouseButtonReleased(1)) {
            if (ct.active) {
                if (ct.objecttype == "ball") {
                    ballcollide b = ct.finishcreationb(mousepos);
                    if (b.get_r() > 1) {
                        balls.push_back(b);
                    }
                    ballcount = balls.size();
                }
                else if (ct.objecttype == "rect") {
                    rectcollide r = ct.finishcreationr(mousepos);
                    if (r.get_xsize() > 1 and r.get_ysize() > 1) {
                        boxes.push_back(ct.finishcreationr(mousepos));
                    }
                    boxcount = boxes.size();
                }

            }
        }
        if (IsMouseButtonPressed(2)) {
            if (ct.objecttype == "ball") {
                ct.objecttype = "rect";
            }
            else {
                ct.objecttype = "ball";
            }
        }

        if (IsKeyPressed(KEY_SPACE)) {
            for (int i = 0; i < 397; i++) {
                balls.push_back(ballcollide(GetRandomValue(8, 16), GetRandomValue(10, 990), GetRandomValue(10, 990)));
            }
            for (int i = 0; i < 100; i++) {
                balls.push_back(ballcollide(GetRandomValue(16, 34), GetRandomValue(10, 990), GetRandomValue(10, 990)));
            }
            for (int i = 0; i < 3; i++) {
                balls.push_back(ballcollide(GetRandomValue(34, 70), GetRandomValue(10, 990), GetRandomValue(10, 990)));
            }
            ballcount = balls.size();
        }
        if (IsKeyPressed(KEY_B)) {
            for (int i = 0; i < 457; i++) {
                balls.push_back(ballcollide(GetRandomValue(11, 13), GetRandomValue(10, 990), GetRandomValue(10, 990)));
            }
            ballcount = balls.size();
        }
        if (IsKeyPressed(KEY_W)) {
            balls.push_back(ballcollide(GetRandomValue(8, 12), 850, 930, 1750, GetRandomValue(-5, -1), GetRandomValue(-5, -1)));
            ballcount = balls.size();
        }
        if (IsKeyPressed(KEY_C)) {
            balls.clear();
            boxes.clear();
            balls.shrink_to_fit();
            boxes.shrink_to_fit();
            ballcount = balls.size();
            boxcount = boxes.size();
        }

        if (IsKeyPressed(KEY_R)) {
            cam.set_pos(Vector2{ (float)screenheight / 2, (float)screenwidth / 2 });
            cam.set_zoom(1);
            followedball = -1;
        }

        if (IsKeyDown(KEY_UP)) { cam.changepos(Vector2{ 0, -5 * dt * 60 }); followedball = -1;}

        if (IsKeyDown(KEY_DOWN)) { cam.changepos(Vector2{ 0, 5 * dt * 60 }); followedball = -1;}

        if (IsKeyDown(KEY_LEFT)) { cam.changepos(Vector2{ -5 * dt * 60, 0 }); followedball = -1;}

        if (IsKeyDown(KEY_RIGHT)) { cam.changepos(Vector2{ 5 * dt * 60, 0 }); followedball = -1;}

        if (IsKeyPressed(KEY_EQUAL)) {
            if (followedball >= ballcount - 1) {
                followedball = 0;
            }
            else {
                followedball++;
            }
        }
        if (IsKeyPressed(KEY_MINUS)) {
            if (followedball <= 0) {
                followedball = ballcount - 1;
            }
            else {
                followedball--;
            }
        }
        if (IsKeyPressed(KEY_ZERO)) {
            followedball = -1;
        }

        if (followedball > ballcount - 1) {
            followedball = -1;
        }

        int scroll = GetMouseWheelMove();
        if (scroll != 0) { cam.changezoom(pow(1.1, scroll)); }

        gravcontrol.update(gravity, mousepos, mousedown, IsMouseButtonUp(0));

        if (updatefirst) {
            //UPDATING --------------------------------------------

            for (int i = 0; i < ballcount; i++) {//update every rigidbody
                balls.at(i).update(gravity, mousepos, IsMouseButtonPressed(0), IsMouseButtonReleased(0));
            }
            for (int i = 0; i < boxcount; i++) {//update every rigidbody
                boxes.at(i).update(gravity, mousepos, IsMouseButtonPressed(0), IsMouseButtonReleased(0));
            }
        }

        //each object gets updated, then compared in one go
        /*for (int i = 10; i > 0; i--) { // updates multiple times a frame
            for (int i = 0; i < ballcount - 1; i++) {//updates velocities
                ballcollide* current = &balls.at(i);
                current->update(gravity, mousepos, IsMouseButtonPressed(0), IsMouseButtonReleased(0));
                for (int j = i + 1; j < balls.size(); j++) {
                    ballcollide* compare = &balls.at(j);

                    current->ballcollision(compare, gravity);
                }
            }
            if (ballcount > 0) {
                ballcollide* last = &balls.at(ballcount - 1);
                last->update(gravity, mousepos, IsMouseButtonPressed(0), IsMouseButtonReleased(0));
            }
        }*/

        //COLLISION TESTS ---------------------------------------------
        for (int i = 14; i > 0; i--) { // updates multiple times a frame
            if (!balls.empty()) {
                balls.at(0).walls();
            }
            for (int i = 0; i < ballcount - 1; i++) {
                ballcollide* current = &balls.at(i);
                for (int j = i + 1; j < ballcount; j++) {
                    ballcollide* compare = &balls.at(j);

                    current->ballcollision(compare, gravity);;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
                    current->ballposition(compare);
                    compare->walls();
                }
            }

            if (!boxes.empty()) {
                boxes.at(0).walls();
            }
            for (int i = 0; i < boxcount - 1; i++) {
                rectcollide* current = &boxes.at(i);
                for (int j = i + 1; j < boxcount; j++) {
                    rectcollide* compare = &boxes.at(j);

                    current->rectcollision(compare);;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
                    current->rectposition(compare);
                    compare->walls();
                }
            }
            
            for (int i = 0; i < boxcount; i++) {
                rectcollide* current = &boxes.at(i);
                for (int j = 0; j < ballcount; j++) {
                    ballcollide* compare = &balls.at(j);

                    current->rectballcollision(compare);
                    current->rectballposition(compare);
                }
            }
        }

        if (!updatefirst) {
            //UPDATING --------------------------------------------

            for (int i = 0; i < ballcount; i++) {//update every rigidbody
                balls.at(i).update(gravity, mousepos, IsMouseButtonPressed(0), IsMouseButtonReleased(0));
            }
            for (int i = 0; i < boxcount; i++) {//update every rigidbody
                boxes.at(i).update(gravity, mousepos, IsMouseButtonPressed(0), IsMouseButtonReleased(0));
            }
        }

        if (followedball >= 0) {
            cam.set_pos(balls.at(followedball).get_pos());
        }

        BeginDrawing();

            Vector2 zz = cam.worldtocamspace(Vector2{ 0, 0 });
            Vector2 zo = cam.worldtocamspace(Vector2{ 0, 1000 });
            Vector2 oz = cam.worldtocamspace(Vector2{ 1000, 0 });
            Vector2 oo = cam.worldtocamspace(Vector2{ 1000, 1000 });

            ClearBackground(BLACK);

            DrawRectangle(zz.x, zz.y, cam.rescale(screenwidth), cam.rescale(screenheight), LIGHTGRAY);

            ct.draw(mousepos, cam);

            for (int i = 0; i < ballcount; i++) {
                balls.at(i).draw(cam);
            }
            for (int i = 0; i < boxcount; i++) {
                boxes.at(i).draw(cam);
            }

            DrawText(TextFormat("%f", dt), 3, 3, 20, WHITE);
            DrawText(TextFormat("%i", fps), 950, 3, 20, WHITE);

            DrawLine(490, 500, 510, 500, BLACK);
            DrawLine(500, 490, 500, 510, BLACK);

            DrawLine(zz.x, zz.y, zo.x, zo.y, BLACK);
            DrawLine(zo.x, zo.y, oo.x, oo.y, BLACK);
            DrawLine(oo.x, oo.y, oz.x, oz.y, BLACK);
            DrawLine(oz.x, oz.y, zz.x, zz.y, BLACK);

            DrawText("Gravity", 60, 20, 10, BLACK);

            gravcontrol.draw(cam);

            DrawTextureEx(wizard, cam.worldtocamspace(Vector2{ (float)screenwidth - wizard.width, (float)screenheight - wizard.width }), 0, cam.rescale(1), WHITE);
            DrawTextureEx(wizard, cam.worldtocamspace(Vector2{ (float)screenwidth - wizard.width, (float)screenheight - wizard.width }), 0, cam.rescale(1), WHITE);

        EndDrawing();
    }

    UnloadTexture(wizard);
    UnloadTexture(wizardshadow);

    CloseWindow();

    return 0;
}
