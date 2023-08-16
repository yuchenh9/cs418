#version 300 es

layout(location=0) in vec4 position;
layout(location=1) in vec3 normal;
out vec3 vnormal;

uniform float seconds;
uniform mat4 p;
uniform mat4 v;
out vec4 vColor;

void main() {

    vColor = color;
    gl_Position = p*v * vec4(
        position.xy,
        position.zw
    );
    vnormal = mat3(v) * normal;
}

#version 300 es
layout(location=0) in vec4 position;
layout(location=1) in vec3 normal;
uniform mat4 mv;
uniform mat4 p;
out vec3 vnormal;
void main() {
    gl_Position = p * mv * position;
    vnormal = mat3(mv) * normal;
}