
const PNG = require('pngjs').PNG;
const fs = require('fs');

const filePath = 'output2.txt'; // Replace this with the actual path to your text file
function parseString(str) {//helper
  // Split the input string by newline character
  const rows = str.trim().split('\n');
  
  // Initialize the result array
  const result = [];

  // Iterate through the rows and process each one
  for (const row of rows) {
    // Split the row by comma and brackets to get the individual elements
    const elements = row.split(/\]\s*,\s*\[/).map(e => e.replace(/\[|\]/g, '').split(',').map(Number));

    // Add the elements to the result array
    result.push(elements);
  }

  return result;
}
const createRGBA = (r, g, b, a) => {//helper
  // Ensure that the input values are within the valid range (0-255)
  const clamp = (value) => Math.min(255, Math.max(0, value));

  // Clamp the input values for R, G, B, and A
  const red = clamp(r);
  const green = clamp(g);
  const blue = clamp(b);
  const alpha = clamp(a);

  // Use bitwise left shift and bitwise OR operators to construct the 32-bit integer
  const rgba = (alpha << 24) | (red << 16) | (green << 8) | blue;

  return rgba;
};
//main
fs.readFile(filePath, 'utf8', function(err, data) {
  if (err) {
    console.error(err);
    return;
  }

  const fileContent = data; // The file content as a string
  const array=parseString(fileContent)
  //console.log(array[3][2])

  const height = array.length;
  const width = array[0].length;
  

let png = new PNG({
    width: width,
    height: height,
    filterType: -1
});
for (let y = 0; y < png.height; y++) {
  for (let x = 0; x < png.width; x++) {
      let idx = (png.width * y + x) << 2;

      // RGBA values range from 0 - 255
      png.data[idx] = 255;     // red
      png.data[idx+1] = 255;   // green
      png.data[idx+2] = 255;        // blue
      png.data[idx+3] = 255;      // alpha (opacity)
  }
}

for (let y = 0; y < png.height; y++) {
    for (let x = 0; x < png.width; x++) {
        let idx = (png.width * y + x) << 2;
        if(array[y][x][3]!=0){
          // RGBA values range from 0 - 255
          png.data[idx] = array[y][x][0];     // red
          png.data[idx+1] = array[y][x][1];   // green
          png.data[idx+2] = array[y][x][2];        // blue
          png.data[idx+3] = array[y][x][3];      // alpha (opacity)
        }
    }
}


png.pack().pipe(fs.createWriteStream('test.png'));
});
