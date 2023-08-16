#version 300 es
in vec4 position;
in vec4 color;
in vec3 normal;
uniform mat4 v;
uniform mat4 p;
out vec3 vnormal;
out vec4 vColor;
void main() {
    gl_Position = p * v * position;
    vnormal =  normal;
    vColor=color;
}