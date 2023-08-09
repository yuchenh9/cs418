#version 300 es
precision highp float;

in vec4 vColor;
uniform float seconds;
out vec4 fragColor;
in vec4 position2;
vec4 myvec=vec4(1,1,1,1);
void main() {
    float x = gl_FragCoord.x / 300.0; // Assuming a window width of 800 pixels
    float y = gl_FragCoord.y / 300.0; // Assuming a window height of 600 pixels

    fragColor = vec4(cos(sin(seconds*cos(y))), acos(sin(seconds*cos(x))), tan((sqrt(seconds*cos(x)-y))*sin((seconds*cos(x)-y))),seconds); // The color varies from black to yellow across the screen

}
