#version 300 es


in vec4 position;
in vec4 color;
uniform float seconds;
uniform mat4 m;
uniform mat4 p;
out vec4 vColor;
out vec4 position2;
out float seconds2;

void main() {
    vColor = color*cos(seconds);
    gl_Position =  vec4(
        position.xy,
        position.zw
    );
}
