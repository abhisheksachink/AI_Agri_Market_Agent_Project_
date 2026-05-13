/**
 * Auth Middleware - Optional JWT token verification
 */

const jwt = require('jsonwebtoken');

module.exports = function(req, res, next) {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    
    if (token) {
        try {
            const decoded = jwt.verify(token, process.env.JWT_SECRET);
            req.user = { id: decoded.id };
        } catch (err) {
            // Token invalid, but continue as anonymous
            req.user = { id: 'anonymous' };
        }
    } else {
        // No token, continue as anonymous
        req.user = { id: 'anonymous' };
    }
    
    next();
};
