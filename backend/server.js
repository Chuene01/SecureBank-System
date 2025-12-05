const express = require("express");
const mongoose = require("mongoose");
const path = require("path");
const cors = require("cors");

const app = express();

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

// Connect to MongoDB
mongoose.connect("mongodb+srv://kagisomasebe98_db_user:2zmolbXZzHvXmolJ@cluster0.yutvibh.mongodb.net/banking-system")
    .then(() => console.log("✅ MongoDB Connected Successfully"))
    .catch(err => console.error("❌ MongoDB Connection Error:", err));

// Import routes
const registerRoutes = require("./routes/register.js");

// Use routes
app.use("/", registerRoutes);

// ⭐ START SERVER
app.listen(5000, () => {
    console.log("🚀 Server running on http://localhost:5000");
    console.log("📁 Serving static files from:", path.join(__dirname, "public"));
});