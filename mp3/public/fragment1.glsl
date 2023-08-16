#version 300 es
precision highp float;
uniform vec3 lightdir;
out vec4 fragColor;
in vec3 vnormal;
in vec4 vColor;
void main() {
    //float lambert = dot(normalize(vnormal), lightdir);
    fragColor = vec4(vColor.rgb, 1);
    
}