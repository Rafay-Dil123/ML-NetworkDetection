import { spawn } from "child_process";
import path from "path";
import fs from "fs"; // Import fs module to read/write files

export default function handler(req, res) {
  // Path to the results.json file
  const resultsFilePath = path.join(process.cwd(), 'results.json');
  
  // Path to the Python script
  const scriptPath = path.join(process.cwd(), 'models/train_model.py');

  // Run the Python script
  const python = spawn('python', [scriptPath]);

  // // Collect data from Python script's stdout
  // python.stdout.on("data", (data) => {
  //   // Write the output to results.json while script runs
  //   fs.writeFileSync(resultsFilePath, data);
  // });

  // Handle errors from Python script
  python.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  // When the Python script finishes
  python.on("close", (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: "Python script failed to execute" });
    }

    // After Python script execution, read the results from results.json
    try {
      const rawResults = fs.readFileSync(resultsFilePath, "utf-8");
      const results = JSON.parse(rawResults);

      // Clear the results.json file after reading
      fs.writeFileSync(resultsFilePath, JSON.stringify({}));

      // Send the results as the response
      res.status(200).json(results); // Send the parsed results from results.json
    } catch (error) {
      // Handle errors in reading or parsing the results.json file
      console.error("Error reading or processing results.json:", error);
      res.status(500).json({ error: "Failed to read or process results.json" });
    }
  });
}
