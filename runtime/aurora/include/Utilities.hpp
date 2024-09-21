#pragma once

#include <cstdint>

namespace renpy {
template<typename T>
struct Tvec2 {
    Tvec2(T newX, T newY)
       : x(newX)
       , y(newY)
    {}

    T x;
    T y;
};

using ivec2 = Tvec2<int32_t>;
using vec2 = Tvec2<float>;

float degreesToRadians(float degrees);

vec2 rotateUV(const vec2& uv, float rotation);

} // namespace renpy
