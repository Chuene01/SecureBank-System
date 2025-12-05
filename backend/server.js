const express = require("express");
const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");
const path = require("path");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static HTML
app.use(express.static(path.join(__dirname, "public")));

// Connect to MongoDB
mongoose.connect("mongodb+srv://kagisomasebe98_db_user:2zmolbXZzHvXmolJ@cluster0.yutvibh.mongodb.net/banking-system")
    .then(() => console.log("✅ MongoDB Connected Successfully"))
    .catch(err => console.error("❌ MongoDB Connection Error:", err));

// Import the CORRECT User model (from models folder)
const User = require("./models/register.js");

// ⭐ REGISTER USER
app.post("/register", async (req, res) => {
    try {
        const { username, email, password, confirm } = req.body;

        if (!username || !email || !password || !confirm) {
            return res.status(400).send("❌ All fields are required.");
        }

        if (password !== confirm) {
            return res.status(400).send("❌ Passwords do not match.");
        }

        // Check if user exists
        const existingUser = await User.findOne({ 
            $or: [{ email }, { username }] 
        });
        
        if (existingUser) {
            return res.status(400).send("❌ User already exists.");
        }

        // Create user using the model from models folder
        const newUser = new User({
            username,
            email,
            password
        });

        await newUser.save();

        return res.redirect("/Login.html");

    } catch (error) {
        console.error("Registration error:", error);
        return res.status(500).send("❌ Registration failed: " + error.message);
    }
});

// ⭐ START SERVER
app.listen(5000, () => {
    console.log("🚀 Server running on http://localhost:5000");
});