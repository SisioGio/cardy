import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../utils/AuthContext";

const MainNav = () => {
  const { logout, auth } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  const handleLinkClick = () => setIsOpen(false);

  return (
    <nav className="fixed top-0 left-0 w-full shadow-xl h-20 z-50 backdrop-blur-md bg-gradient-to-r from-red-600 via-pink-500 to-purple-600 bg-opacity-90 rounded-b-md transition-all duration-300 ease-in-out">
      <div className="mx-auto flex justify-between items-center px-6 h-full">
        {/* Logo */}
        <Link to="/" className="text-3xl font-extrabold text-white tracking-wide hover:text-yellow-400 transition duration-300 transform neon-text">
          Restaurant Explorer
        </Link>

        {/* Mobile Menu Button */}
        <button
          className="xl:hidden text-white text-3xl focus:outline-none hover:text-yellow-400 transition duration-300"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle menu"
        >
          ☰
        </button>

        {/* Navigation Links */}
        <ul className={`z-30 absolute xl:static top-20 left-0 w-full xl:w-auto bg-black xl:bg-transparent xl:flex xl:items-center xl:space-x-6 px-6 py-4 xl:px-0 transition-all duration-300 ease-in-out transform ${isOpen ? "block" : "hidden xl:flex"}`}>
          <li className="py-3 px-2 text-center hover:text-gold transition duration-300 transform relative hover:bg-indigo-700 rounded-lg hover:bg-opacity-30">
            <Link to="/" onClick={handleLinkClick} className="text-white text-xl font-light hover:text-gray-100">
              Home
            </Link>
          </li>
          <li className="py-3 px-2 text-center hover:text-gold transition duration-300 transform relative hover:bg-indigo-700 rounded-lg hover:bg-opacity-30">
            <Link to="/Explorer" onClick={handleLinkClick} className="text-white text-xl font-light hover:text-gray-100">
              Explorer
            </Link>
          </li>
          {auth && (
            <li className="py-3 px-2 text-center hover:text-gold transition duration-300 transform relative hover:bg-indigo-700 rounded-lg hover:bg-opacity-30">
              <button onClick={logout} className="text-white text-xl font-light hover:text-gray-100">
                Logout
              </button>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default MainNav;