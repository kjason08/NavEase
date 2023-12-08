const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');
const { spawn } = require("child_process");

const app = express();
const port = 3000;

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('/markers', (req, res) => {
    const jsonFilePath = path.join(__dirname, 'data', 'markers.json');
    fs.readFile(jsonFilePath, 'utf8', (err, data) => {
        if (err) {
            res.status(500).send('Error reading the JSON file');
        } else {
            res.json(JSON.parse(data));
        }
    });
});

function runPythonScript(scriptName, inputs) {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', [scriptName, ...inputs]);

        let output = '';
        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
            console.log(output)
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python 스크립트 에러: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Python 스크립트 실행 오류, 코드 ${code}`));
            } else {
                resolve(output);
            }
        });
    });
}

app.post('/getPythonData', async (req, res) => {
    const { value1, value2, value3, value4, value5 } = req.body;
    try {
        const script1Result = runPythonScript('Algorithm.py', [value1, value2, value3, value4, value5]);
        const script2Result = runPythonScript('Algorithm_no_occupancy.py', [value1, value2, value3, value4, value5]);

        const results = await Promise.all([script1Result, script2Result]);
        res.json({ 0: JSON.parse(results[0]), 1: JSON.parse(results[1]) });
    } catch (error) {
        res.status(500).send(error.toString());
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
