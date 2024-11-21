#pragma once
#include <raylib.h>
#include <raymath.h>
#include "include/camera.h"
#include <iostream>

class slider2d
{
	Vector2 size;
	Vector2 pos;

    int handler;

    Vector2 handlepos;
    Vector2 handleval;
    Vector2 min;
    Vector2 max;
    
    bool held;

public:
    slider2d(int xpos, int ypos, int width, int height, float xmin, float xmax, float ymin, float ymax, float startx = 0, float starty = 0) {
        pos = Vector2{ (float)xpos,  (float)ypos };

        min = Vector2{ xmin, ymin };
        max = Vector2{ xmax, ymax };

        size = Vector2{ (float)width, (float)height };

        handleval = Vector2{ startx, starty };
        Vector2Clamp(handleval, min, max);

        valtopos();

        handler = 10;

        held = false;
    }

    void valtopos() {
        Vector2 normalised = Vector2Divide(Vector2Subtract(handleval, min), Vector2Subtract(max, min));

        handlepos = Vector2Add(Vector2Multiply(normalised, size), pos);
    }

    void postoval() {
        Vector2 normalised = Vector2Divide(Vector2Subtract(handlepos, pos), size);

        handleval = Vector2Add(Vector2Multiply(normalised, Vector2Subtract(max, min)), min);
    }

    void update(Vector2& var, Vector2 mousepos, bool mousedown, bool mouseup) {
        float xdif = mousepos.x - handlepos.x;
        float ydif = mousepos.y - handlepos.y;
        
        if (mousedown) {
            float tdif = sqrt(xdif * xdif + ydif * ydif);

            if (tdif < handler) {
                held = true;
            }
        }
        else if (mouseup) {
            held = false;
        }

        if (held) {
            handlepos = Vector2Clamp(mousepos, pos, Vector2Add(pos, size));
            postoval();

            if (abs(handleval.x - (min.x + (max.x - min.x) / 2)) < 0.1) {
                handleval.x = (min.x + (max.x - min.x) / 2);
            }
            if (abs(handleval.y - (min.y + (max.y - min.y) / 2)) < 0.1) {
                handleval.y = (min.y + (max.y - min.y) / 2);
            }

            valtopos();

            std::cout << handleval.x << ", " << handleval.y << "  " << handlepos.x << ", " << handlepos.y << "\n";

            var = handleval;
        }
    }

    void draw(camera cam) {
        DrawLine(pos.x, pos.y + size.y / 2, pos.x + size.x, pos.y + size.y / 2, GRAY);
        DrawLine(pos.x + size.x / 2, pos.y, pos.x + size.x / 2, pos.y + size.y, GRAY);

        DrawCircleV(handlepos, handler, BLACK);
        Rectangle rec;
        rec.x = pos.x - handler;
        rec.y = pos.y - handler;
        rec.width = size.x + 2 * handler;
        rec.height = size.y + 2 * handler;
        DrawRectangleRoundedLines(rec, 0.17, 16, 2, BLACK);
    }
};

