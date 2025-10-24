import mongoose, { Document, Schema, Model } from "mongoose";

// User Interface
export interface IUser extends Document {
    name: string;
    email: string;
    password: string;
    city?: string;
    state?: string;
    country?: string;
    role: "user" | "admin" | "superadmin";
    createdAt?: Date;
    updatedAt?: Date;
}

// User Schema
const UserSchema: Schema<IUser> = new Schema (
    {
        name: { type: String, required: true, min: 2, max: 100 },
        email: { type: String, required: true, max: 50, unique: true },
        password: { type: String, required: true, min: 5 },
        city: { type: String },
        state: { type: String },
        country: { type: String },
        role: {
            type: String,
            enum: ["user", "admin", "superadmin"],
            default: "admin",
        },
    },
    { timestamps: true }
);

// Create and export the model
const User: Model<IUser> =
    mongoose.models.User || mongoose.model<IUser>("User", UserSchema);

export default User;