import express from "express";
import cors from "cors";
import csv from "csvtojson";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
app.use(cors());

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ← This is the correct spot for your CSV reading code
app.get("/api/products", async (req, res) => {
  try {
    const filePath = path.join(__dirname, "./data/cleaned_beauty.csv");
    const jsonArray = await csv().fromFile(filePath); // Reads CSV
    res.json(jsonArray); // Sends JSON to frontend
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = 5002;
app.listen(PORT, () => console.log("Backend running on port 5002"));
