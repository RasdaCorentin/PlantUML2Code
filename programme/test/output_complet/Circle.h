#ifndef CIRCLE_H
#define CIRCLE_H

#include "Shape.h"
#include "Drawable.h"

class Circle : public Shape, public Drawable {
public:
    double getArea();
    void draw();
private:
    double radius;
};

#endif