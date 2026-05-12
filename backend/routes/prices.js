/**
 * Prices Routes - Price information endpoints
 */

const express = require('express');
const router = express.Router();
const axios = require('axios');

// Get sell advice
router.post('/sell-advice', async (req, res) => {
    const { crop, currentPrice, quantity, costPrice, state } = req.body;
    
    try {
        const response = await axios.post(
            `${process.env.AI_SERVICE_URL}/api/sell-advice`,
            {
                crop,
                current_price: currentPrice,
                quantity,
                cost_price: costPrice,
                state
            }
        );
        
        res.json(response.data);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
