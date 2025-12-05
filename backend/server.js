require('dotenv').config(); // Add this at the VERY TOP of the file
const express = require("express");
const mongoose = require("mongoose");
const path = require("path");
const cors = require("cors");

const app = express();

// Load environment variables
const PORT = process.env.PORT || 5000;
const MONGODB_URI = process.env.MONGODB_URI;

// Validate that environment variables are set
if (!MONGODB_URI) {
    console.error("❌ ERROR: MONGODB_URI is not defined in environment variables");
    console.error("   Please create a .env file with MONGODB_URI");
    process.exit(1);
}

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ✅ Serve static files from public directory
app.use(express.static(path.join(__dirname, "public")));

// ✅ Add a specific route for the root to serve index/register page
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "Register.html"));
});

// ✅ Add route for Login.html
app.get("/Login.html", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "Login.html"));
});

// Connect to MongoDB using environment variable
mongoose.connect(MONGODB_URI)
    .then(() => console.log("✅ MongoDB Connected Successfully"))
    .catch(err => {
        console.error("❌ MongoDB Connection Error:", err.message);
        console.error("   Check your MONGODB_URI in .env file");
    });

// Import routes
const registerRoutes = require("./routes/register.js");

// Use routes
app.use("/", registerRoutes);

// ⭐ START SERVER
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
    console.log("📁 Serving static files from:", path.join(__dirname, "public"));
    console.log("🔐 Using environment variables from .env file");
});