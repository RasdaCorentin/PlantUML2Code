#ifndef SHAPE_H
#define SHAPE_H

#include "Canvas.h"
#include "Color.h"

// Classe abstraite de base pour toutes les formes
class Shape {
public:
    double getArea();
    void move();
private:
    String color;
    int x;
    int y;
    // agregation avec Canvas
    Canvas* canvas;
    // association avec Color
    Color* color;
};

#endif