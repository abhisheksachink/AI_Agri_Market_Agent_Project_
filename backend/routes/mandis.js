/**
 * Mandi Routes - Mandi information endpoints
 */

const express = require('express');
const router = express.Router();
const axios = require('axios');

// Get mandi prices
router.get('/prices/:crop/:state', async (req, res) => {
    const { crop, state } = req.params;
    
    try {
        const response = await axios.get(
            `${process.env.AI_SERVICE_URL}/api/mandi-prices`,
            {
                params: { crop, state }
            }
        );
        
        res.json(response.data);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
