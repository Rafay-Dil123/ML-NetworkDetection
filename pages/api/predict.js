
import { spawn } from 'child_process';
import path from 'path';

export default function handler(req, res) {
  if (req.method === 'POST') {
    const scriptPath = path.join(process.cwd(), 'models/train_model.py');
    const python = spawn('python', [scriptPath]);

    let output = ''; // Collect script output

    python.stdout.on('data', (data) => {
      output += data.toString(); // Accumulate stdout
    });

    python.stderr.on('data', (data) => {
      console.error(data.toString()); // Log errors
    });

    python.on('close', (code) => {
      if (code === 0) {
        res.status(200).json({ success: true, output }); // Return script output
      } else {
        res.status(500).json({ success: false, error: 'Training failed.' });
      }
    });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
