#include "Utilities.hpp"

#include <algorithm>
#include <math.h>

namespace renpy {

vec2 rotateUV(const vec2& uv, float rotation)
{
    float mid = 0.5;

    return vec2(std::cos(rotation) * (uv.x - mid) + std::sin(rotation) * (uv.y - mid) + mid,
                std::cos(rotation) * (uv.y - mid) - std::sin(rotation) * (uv.x - mid) + mid);
}

float degreesToRadians(float degrees)
{
    constexpr auto kPi = 3.14159265358979323846264;
    return degrees * (kPi / 180.0);
}

} // namespace renpy
