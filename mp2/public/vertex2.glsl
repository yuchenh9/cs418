#version 300 es

in vec4 position;
in vec4 color;

uniform float seconds;
uniform mat4 m;
uniform mat4 p;
uniform mat4 v;
out vec4 vColor;

void main() {

    vColor = color;
    gl_Position = p*v * vec4(
        position.xy,
        position.zw
    );
}
