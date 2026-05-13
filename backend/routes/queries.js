/**
 * Query Routes - Handle user queries
 */

const express = require('express');
const router = express.Router();
const axios = require('axios');
const Query = require('../models/Query');
const auth = require('../middleware/auth');

// Process query (no auth required)
router.post('/', auth, async (req, res) => {
    const { query, language, latitude, longitude } = req.body;
    
    try {
        // Call AI service
        const aiResponse = await axios.post(
            `${process.env.AI_SERVICE_URL}/api/query`,
            {
                query,
                language,
                latitude,
                longitude
            }
        );
        
        // Save to database only if user is authenticated
        if (req.user.id !== 'anonymous') {
            const savedQuery = new Query({
                userId: req.user.id,
                query,
                language,
                intent: aiResponse.data.intent,
                crop: aiResponse.data.crop,
                location: aiResponse.data.location,
                response: {
                    english_answer: aiResponse.data.english_answer,
                    hindi_answer: aiResponse.data.hindi_answer,
                    confidence_score: aiResponse.data.confidence_score,
                    mandi_prices: aiResponse.data.live_mandi_prices,
                    trend_analysis: aiResponse.data.trend_analysis,
                    prediction: aiResponse.data.prediction,
                    sources: aiResponse.data.sources
                }
            });
            
            await savedQuery.save();
        }
        
        res.json(aiResponse.data);
    } catch (err) {
        console.error('Query error:', err);
        res.status(500).json({
            success: false,
            error: err.message
        });
    }
});

// Get user's query history (requires auth)
router.get('/history', auth, async (req, res) => {
    try {
        if (req.user.id === 'anonymous') {
            return res.json({
                success: true,
                queries: [],
                message: 'Login to view query history'
            });
        }
        
        const queries = await Query.find({ userId: req.user.id })
            .sort({ createdAt: -1 })
            .limit(50);
        
        res.json({
            success: true,
            queries
        });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;
