#ifndef CANVAS_H
#define CANVAS_H

#include <vector>
#include "Shape.h"

// Conteneur principal
class Canvas {
public:
    void render();
private:
    String name;
    // agregation avec Shape
    std::vector<Shape*> shapeList;
};

#endif