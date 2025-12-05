// controllers/login.js
const express = require('express');
const router = express.Router();
const User = require('../models/register'); // Path to your User model
const bcrypt = require('bcrypt');

// POST /login
router.post('/', async (req, res) => {
    try {
        const { email, password } = req.body;

        // Check for missing fields
        if (!email || !password) {
            return res.status(400).send('All fields are required');
        }

        // Find user by email
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).send('Invalid email or password');
        }

        // Compare password
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).send('Invalid email or password');
        }

        // Login successful
        // For demo: redirect to dashboard
        return res.redirect('/dashboard.html');

    } catch (error) {
        console.error(error);
        return res.status(500).send('Server error');
    }
});

module.exports = router;
