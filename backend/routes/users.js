/**
 * Users Routes - User profile management
 */

const express = require('express');
const router = express.Router();
const User = require('../models/User');
const auth = require('../middleware/auth');

// Get profile
router.get('/profile', auth, async (req, res) => {
    try {
        const user = await User.findById(req.user.id).select('-password');
        res.json(user);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Update profile
router.put('/profile', auth, async (req, res) => {
    const { name, phone, state, district, cropsProduce } = req.body;
    
    try {
        let user = await User.findById(req.user.id);
        
        if (name) user.name = name;
        if (phone) user.phone = phone;
        if (state) user.state = state;
        if (district) user.district = district;
        if (cropsProduce) user.cropsProduce = cropsProduce;
        
        user.updatedAt = Date.now();
        await user.save();
        
        res.json({
            success: true,
            user
        });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
