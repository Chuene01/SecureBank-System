const express = require("express");
const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");
const path = require("path");
const User = require("./register.js");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static HTML
app.use(express.static(path.join(__dirname, "public")));

// ⭐ CONNECT TO MONGO — paste your FULL connection string here
mongoose.connect("mongodb+srv://kagisomasebe98_db_user:2zmolbXZzHvXmolJ@cluster0.yutvibh.mongodb.net/")
    .then(() => console.log("✅ MongoDB Connected Successfully"))
    .catch(err => console.error("❌ MongoDB Connection Error:", err));

// ⭐ REGISTER USER
app.post("/register", async (req, res) => {
    try {
        const { username, email, password, confirm } = req.body;

        if (password !== confirm) {
            return res.send("❌ Passwords do not match.");
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        await User.create({
            username,
            email,
            password: hashedPassword
        });

        return res.redirect("/Login.html");

    } catch (error) {
        console.log(error);
        return res.send("❌ Registration failed.");
    }
});

// ⭐ START SERVER
app.listen(5000, () => {
    console.log("🚀 Server running on http://localhost:5000");
});
