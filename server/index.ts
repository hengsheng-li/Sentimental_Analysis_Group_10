// BACKEND SETUP
import express, { Application } from 'express';
import bodyParser from 'body-parser';
import mongoose from 'mongoose';
import cors from 'cors';
import dotenv from 'dotenv';
import helmet from 'helmet';
import morgan from 'morgan';
import mainRoutes from './routes/main';
import insightsRoutes from './routes/insights';

// DATA IMPORTS
import Product from './models/Product';
import ProductStat from './models/ProductStat';
//import User from "../models/User.ts";
//import { dataProduct, dataProductStat } from './data/index';

// CONFIGURATIONS
dotenv.config();
const app: Application = express();

app.use(express.json());
app.use(helmet());
app.use(helmet.crossOriginResourcePolicy({ policy : "cross-origin"}))
app.use(morgan('common'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended : false}));
app.use(cors());

// ROUTES
app.use("/main", mainRoutes);
app.use("/insights", insightsRoutes);

// MONGOOSE SETUP - Connects to Mongoose and Mongoose database
const PORT: number = Number(process.env.PORT) || 9000; // back-up port if needed

mongoose
    .connect(process.env.MONGO_URL || '')
    .then(() => {
        app.listen(PORT, () => console.log(`Server Port: ${PORT}`));

        Product.insertMany(dataProduct).catch(err => 
            console.log('Product insert failed:', err)
        );
        ProductStat.insertMany(dataProductStat).catch(err =>
            console.log('ProductStat insert failed:', err)
        );
    })
    .catch((error) => console.log(`${error} did not connect`))