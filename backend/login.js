// backend/login.js
const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const User = require('./models/User'); // Correct path

// POST /login
router.post('/', async (req, res) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) return res.status(400).send('All fields are required');

        const user = await User.findOne({ email });
        if (!user) return res.status(400).send('Invalid email or password');

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) return res.status(400).send('Invalid email or password');

        // Successful login: redirect to dashboard
        res.redirect('/dashboard.html');
    } catch (error) {
        console.error(error);
        res.status(500).send('Server error');
    }
});

module.exports = router;
