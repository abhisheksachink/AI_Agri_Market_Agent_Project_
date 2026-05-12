/**
 * Query Model - Store user queries and responses
 */

const mongoose = require('mongoose');

const querySchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    query: {
        type: String,
        required: true
    },
    language: {
        type: String,
        enum: ['en', 'hi', 'auto'],
        default: 'auto'
    },
    intent: String,
    crop: String,
    location: String,
    response: {
        english_answer: String,
        hindi_answer: String,
        confidence_score: Number,
        mandi_prices: [Object],
        trend_analysis: Object,
        prediction: Object,
        sources: [String]
    },
    helpful: Boolean,
    feedback: String,
    createdAt: {
        type: Date,
        default: Date.now
    }
});

module.exports = mongoose.model('Query', querySchema);
