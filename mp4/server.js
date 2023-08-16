const express = require('express');
const { spawn } = require('child_process');
const app = express();
const path = require('path');

// Serve static files from the "public" folder
app.use(express.static(path.join(__dirname, 'public')));

// Define a route to send the HTML file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'several.html'));
});

// Start the server
const port = 3000;

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
