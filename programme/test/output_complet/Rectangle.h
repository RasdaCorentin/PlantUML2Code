#ifndef RECTANGLE_H
#define RECTANGLE_H

#include "Shape.h"
#include "Drawable.h"

class Rectangle : public Shape, public Drawable {
public:
    double getArea();
    void draw();
private:
    double width;
    double height;
};

#endif