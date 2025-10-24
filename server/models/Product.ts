import mongoose, { Document, Schema, Model } from "mongoose";

// Interface to represent the structure of the Products page
export interface IProduct extends Document {
    name: string;               // name of the product
    price: number;              // price of the product
    description: string;        // description of the product
    category: string;           // category this product belongs to ("Electronics")
    rating: number;             // Average rating of this product
    supply: number;             // Amount of this product in stock
    createdAt?: Date;           // Auto-generated timestamp when created
    updatedAt?: Date;           // Auto-generated timestamp when updated
}

// Mongoose schema for the product model
// Schema defines how the data is structured and validated in MongoDB
const ProductSchema: Schema<IProduct> = new Schema (
    {
    name: { type: String, required: true },
    price: { type: Number, required: true },
    description: { type: String, required: true },
    category: { type: String, required: true },
    rating: { type: Number, required: true },
    supply: { type: Number, required: true },
    },
    { timestamps: true}        // Automatically adds createdAt and updatedAt fields
);

// Create and export the model
const Product: Model<IProduct> =
    mongoose.models.Product || mongoose.model<IProduct>("Product", ProductSchema);

export default Product;