const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');

const app = express();
const port = 3001;

app.use(express.static('public'));
app.use(cors());

app.post('/run-script', (req, res) => {
  const pythonProcess = exec('python main.py');

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Script output: ${data}`);
    res.write(`Script output: ${data}<br>`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Script error: ${data}`);
    res.write(`Script error: ${data}<br>`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Script execution finished with code ${code}`);
    res.end(`Script execution finished with code ${code}`);
  });
});

app.listen(port, () => {
  console.log(`Server is running on https://wikimotivate.onrender.com:${port}`);
});
