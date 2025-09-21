/* BACKEND SETUP */
import express from 'express';
import bodyParser from 'body-parser';
import mongoose from 'mongoose';
import cors from 'cors';
import dotenv from 'dotenv';
import helmet from 'helmet';
import morgan from 'morgan';
import mainRoutes from "./routes/main.js";
import insightsRoutes from "./routes/insights.js";


/* Congigurations */
dotenv.config();
const app = express();
app.use(express.json());
app.use(helmet());
app.use(helmet.crossOriginResourcePolicy({ policy : "cross-origin"}))
app.use(morgan("common"));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended : false}));
app.use(cors());

/* Routes */
app.use("/main", mainRoutes);
app.use("/insights", insightsRoutes);

/* Mongoose Setup - Connects to Mongoose and Mongoose database */
const PORT = process.env.PORT || 9000; // back-up port if needed
mongoose.connect(process.env.MONGO_URL, {
}).then(() => {
    app.listen(PORT, () => console.log(`Server Port: ${PORT}`))
}).catch((error) => console.log(`${error} did not connect`))