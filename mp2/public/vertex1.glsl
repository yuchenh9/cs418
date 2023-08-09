#version 300 es

in vec4 position;
in vec4 color;

uniform float seconds;
uniform mat4 m;
uniform mat4 p;
out vec4 vColor;

void main() {

    vColor = color;
    gl_Position = m * vec4(
        position.xy*cos(seconds*0.6180339887498949),
        position.zw
    );
    //vColor = color;
    // // Determine the displacement based on the vertex ID and time
    //float displacementAmount = sin(float(gl_VertexID) * 0.5 + seconds) * 0.1;
//
    //// Create a displacement vector
    //vec4 displacement = vec4(displacementAmount, displacementAmount, 0.0, 0.0);
//
    //// Apply the displacement to the original position
    //vec4 newPosition = position + displacement;
//
    //// Apply the model-view-projection transformation
    //gl_Position = newPosition;
}
