/**
 * Home Page
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FaRobot, FaChartLine, FaMapMarkerAlt, FaShieldAlt } from 'react-icons/fa';

export default function HomePage() {
  const features = [
    {
      icon: <FaRobot className="text-3xl" />,
      title: 'AI-Powered Insights',
      description: 'Get intelligent recommendations using advanced AI agents'
    },
    {
      icon: <FaChartLine className="text-3xl" />,
      title: 'Price Trends',
      description: 'Analyze price movements and predict future trends'
    },
    {
      icon: <FaMapMarkerAlt className="text-3xl" />,
      title: 'Nearby Markets',
      description: 'Find the best markets near you for your crops'
    },
    {
      icon: <FaShieldAlt className="text-3xl" />,
      title: 'Verified Data',
      description: 'Government verified prices from Agmarknet and eNAM'
    }
  ];

  return (
    <div className="container-custom">
      {/* Hero */}
      <section className="py-20 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-6 gradient-text">
            Smart Agricultural Market Intelligence
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
            AI-powered platform helping farmers make informed decisions about crop prices, market trends, and optimal selling strategies
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              to="/chat"
              className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
            >
              Start Chatting
            </Link>
            <Link
              to="/prices"
              className="px-8 py-3 border-2 border-green-600 text-green-600 rounded-lg hover:bg-green-50 dark:hover:bg-slate-800 transition"
            >
              Check Prices
            </Link>
          </div>
        </motion.div>
      </section>

      {/* Features */}
      <section className="py-16 mb-20">
        <h2 className="text-4xl font-bold text-center mb-12">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="p-6 bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700 hover:shadow-lg transition"
            >
              <div className="text-green-600 mb-4">{feature.icon}</div>
              <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-400">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 text-center bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-lg mb-20">
        <h2 className="text-4xl font-bold mb-6">Ready to Make Better Decisions?</h2>
        <p className="text-lg mb-8 opacity-90">Join thousands of farmers using AgroAI</p>
        <Link
          to="/chat"
          className="px-8 py-3 bg-white text-green-600 rounded-lg font-bold hover:bg-gray-100 transition"
        >
          Get Started Free
        </Link>
      </section>
    </div>
  );
}
