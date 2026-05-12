/**
 * Footer Component
 */

import React from 'react';
import { FaGithub, FaTwitter, FaLinkedin } from 'react-icons/fa';

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-100 mt-20">
      <div className="container-custom py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* About */}
          <div>
            <h3 className="font-bold text-xl mb-4">AgroAI</h3>
            <p className="text-gray-400">
              AI-powered agricultural market intelligence for Indian farmers.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-bold mb-4">Product</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-green-500 transition">Features</a></li>
              <li><a href="#" className="hover:text-green-500 transition">Pricing</a></li>
              <li><a href="#" className="hover:text-green-500 transition">API</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-bold mb-4">Resources</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-green-500 transition">Docs</a></li>
              <li><a href="#" className="hover:text-green-500 transition">Blog</a></li>
              <li><a href="#" className="hover:text-green-500 transition">Support</a></li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h4 className="font-bold mb-4">Follow</h4>
            <div className="flex gap-4">
              <a href="#" className="text-gray-400 hover:text-green-500 transition"><FaGithub size={24} /></a>
              <a href="#" className="text-gray-400 hover:text-green-500 transition"><FaTwitter size={24} /></a>
              <a href="#" className="text-gray-400 hover:text-green-500 transition"><FaLinkedin size={24} /></a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
          <p>&copy; 2024 AI Agricultural Market Intelligence. All rights reserved.</p>
          <p className="text-sm mt-2">M.Tech Research Project | AI & Agriculture</p>
        </div>
      </div>
    </footer>
  );
}
