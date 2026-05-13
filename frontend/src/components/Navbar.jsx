/**
 * Navbar Component
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiMenu, FiX, FiSun, FiMoon } from 'react-icons/fi';
import { FaRobot } from 'react-icons/fa';

export default function Navbar({ theme, onThemeToggle }) {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  return (
    <nav className="sticky top-0 z-50 glass-morphism backdrop-blur-xl border-b border-green-200 dark:border-slate-700">
      <div className="container-custom">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 hover:scale-105 transition">
            <div className="p-2 bg-gradient-to-br from-green-500 to-blue-500 rounded-lg">
              <FaRobot className="text-white text-2xl" />
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">AgroAI</h1>
              <p className="text-xs text-gray-600 dark:text-gray-400">Market Intelligence</p>
            </div>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-8">
            <Link to="/" className="hover:text-green-600 transition">Home</Link>
            <Link to="/chat" className="hover:text-green-600 transition">Chat</Link>
            <Link to="/prices" className="hover:text-green-600 transition">Prices</Link>
            <Link to="/dashboard" className="hover:text-green-600 transition">Dashboard</Link>
          </div>

          {/* Right Actions */}
          <div className="flex items-center gap-4">
            {/* Theme Toggle */}
            <button
              onClick={onThemeToggle}
              className="p-2 hover:bg-gray-200 dark:hover:bg-slate-700 rounded-lg transition"
            >
              {theme === 'light' ? <FiMoon size={20} /> : <FiSun size={20} />}
            </button>



            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2"
            >
              {mobileMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="md:hidden pb-4 border-t border-gray-200 dark:border-slate-700"
          >
            <Link to="/" className="block py-2 hover:text-green-600">Home</Link>
            <Link to="/chat" className="block py-2 hover:text-green-600">Chat</Link>
            <Link to="/prices" className="block py-2 hover:text-green-600">Prices</Link>
            <Link to="/dashboard" className="block py-2 hover:text-green-600">Dashboard</Link>
          </motion.div>
        )}
      </div>
    </nav>
  );
}
