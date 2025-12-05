const bcrypt = require("bcryptjs");
const User = require("../models/register"); // import the User model

// Controller to handle the user registration logic
const registerUser = async (req, res) => {
    try {
        const { username, email, password, confirm } = req.body;

        // Check if all fields are provided
        if (!username || !email || !password || !confirm) {
            return res.status(400).send("All fields are required");
        }

        // Check if passwords match
        if (password !== confirm) {
            return res.status(400).send("Passwords do not match");
        }

        // Check if the email is already registered
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.status(400).send("Email already exists");
        }

        // Hash the password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create a new user and save to database
        const newUser = new User({
            username,
            email,
            password: hashedPassword
        });

        await newUser.save();

        // Return a success response
        return res.status(201).send("User registered successfully");
    } catch (error) {
        console.error(error);
        return res.status(500).send("Server error");
    }
};

module.exports = { registerUser };
