const express = require('express');
const { spawn } = require('child_process');
const app = express();
const path = require('path');

// Serve static files from the "public" folder
app.use(express.static(path.join(__dirname, 'public')));

// Define a route to send the HTML file
//app.get('/', (req, res) => {
//  res.sendFile(path.join(__dirname, 'public', 'index.html'));
//});

// Start the server
const port = 3000;
//app.listen(port, () => {
//  console.log(`Server is running on port ${port}`);
//});
app.get('/', (req, res) => {
  const message = req.query.message || "Dult Message";
  const python = spawn('python', ['script.py', message]);


  python.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).send('Python script failed');
    }

    fs.readFile('output.txt', 'utf8', (err, data) => {
      if (err) {
        console.error(`Error reading file: ${err}`);
        return res.status(500).send('Error reading output');
      }

      res.send(data);
    });
  });

  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
});

app.listen(port, () => {
  console.log(`Server runssning on http://localhost:${port}`);
});
