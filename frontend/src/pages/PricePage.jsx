/**
 * Price Page - Check mandi prices
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';

const crops = ['Tomato', 'Onion', 'Potato', 'Wheat', 'Rice', 'Cotton'];
const states = ['Bihar', 'Punjab', 'Haryana', 'Maharashtra', 'Tamil Nadu', 'Karnataka'];

export default function PricePage() {
  const [selectedCrop, setSelectedCrop] = useState('Tomato');
  const [selectedState, setSelectedState] = useState('Bihar');
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    // Mock prices
    setTimeout(() => {
      setPrices([
        { market: 'Patna APMC', price: 2800, min: 2500, max: 3200 },
        { market: 'Nearby Market 1', price: 2750, min: 2400, max: 3000 },
        { market: 'Nearby Market 2', price: 2900, min: 2600, max: 3400 },
      ]);
      setLoading(false);
    }, 500);
  };

  return (
    <div className="container-custom py-12">
      <h1 className="text-3xl font-bold mb-8">Mandi Price Tracker</h1>

      {/* Search Section */}
      <div className="bg-white dark:bg-slate-800 p-6 rounded-lg border border-gray-200 dark:border-slate-700 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium mb-2">Select Crop</label>
            <select
              value={selectedCrop}
              onChange={(e) => setSelectedCrop(e.target.value)}
              className="w-full"
            >
              {crops.map(crop => (
                <option key={crop} value={crop}>{crop}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Select State</label>
            <select
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
              className="w-full"
            >
              {states.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={handleSearch}
              disabled={loading}
              className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </div>
      </div>

      {/* Prices List */}
      {prices.length > 0 && (
        <div className="grid gap-4">
          {prices.map((price, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white dark:bg-slate-800 p-6 rounded-lg border border-gray-200 dark:border-slate-700 hover:shadow-lg transition"
            >
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="font-bold text-lg">{price.market}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Min: ₹{price.min} | Max: ₹{price.max}
                  </p>
                </div>
                <div className="text-3xl font-bold text-green-600">
                  ₹{price.price}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
