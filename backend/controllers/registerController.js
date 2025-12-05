const User = require("../models/User.js");

exports.registerUser = async (req, res) => {
    try {
        const { username, email, password, confirm } = req.body;

        // Validate input
        if (!username || !email || !password || !confirm) {
            return res.status(400).json({ 
                success: false, 
                message: "All fields are required" 
            });
        }

        if (password !== confirm) {
            return res.status(400).json({ 
                success: false, 
                message: "Passwords do not match" 
            });
        }

        // Check if user already exists
        const existingUser = await User.findOne({ 
            $or: [{ email }, { username }] 
        });

        if (existingUser) {
            return res.status(400).json({ 
                success: false, 
                message: "User with this email or username already exists" 
            });
        }

        // Create new user (password will be hashed by the pre-save middleware)
        const newUser = new User({
            username,
            email,
            password // This will be hashed automatically
        });

        await newUser.save();

        // Redirect or send success response
        return res.status(201).json({ 
            success: true, 
            message: "Registration successful",
            redirect: "/Login.html"
        });

    } catch (error) {
        console.error("Registration error:", error);
        return res.status(500).json({ 
            success: false, 
            message: "Registration failed",
            error: error.message 
        });
    }
};