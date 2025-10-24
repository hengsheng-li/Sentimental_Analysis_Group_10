import mongoose, { Document, Schema, Model } from "mongoose";

// Monthly data structure for each month's sales and units
export interface IMonthlyData {
    month: string;                          // Month Name
    totalSales: number;                     // Total sales for the month
    totalUnits: number;                     // Total units sold for the month
}

// Daily data structure for each day's sales and units
export interface IDailyData {
    date: string;                           // Date (e.g., "2025-10-13")
    totalSales: number;
    totalUnits: number;
}

// ProductStat document interface (main schema type)
export interface IProductStat extends Document {
    productId: string;
    yearlySalesTotal: number;
    yearlyTotalSoldUnits: number;
    year: number;
    monthlyData: IMonthlyData[];            // Array of monthly data
    dailyData: IDailyData[];                // Array of daily data
    createdAt?: Date;                       // Timestamp when created
    updatedAt?: Date;                       // Timestamp when updated
}

// ProductStat schema
const ProductStatSchema: Schema<IProductStat> = new Schema (
    {
        productId: { type: String, required: true },
        yearlySalesTotal: { type: Number, required: true },
        yearlyTotalSoldUnits: { type: Number, required: true },
        year: { type: Number, required: true },
        monthlyData: [
            {
                month: { type: String, required: true },
                totalSales: { type: Number, required: true },
                totalUnits: { type: Number, required: true },
            },
        ],

        // Daily sales data
        dailyData: [
            {
                date: { type: String, required: true },
                totalSales: { type: Number, required: true },
                totalUnits: { type: Number, required: true },
            },
        ],
    },
    { timestamps: true } // Adds createdAt and updatedAt
);

// Create and export model
const ProductStat: Model<IProductStat> =
    mongoose.models.ProductStat || mongoose.model<IProductStat>("ProductStat", ProductStatSchema);

export default ProductStat;