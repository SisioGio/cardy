import React, { useEffect, useState } from 'react';
import './App.css';
import Layout from "./components/Layout";

import Home from "./pages/Home";
import NotFound from "./pages/NotFound";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Explorer from './pages/Explorer';
const App = () => {




  return (


     
      <Layout>
   
        <Routes>
          <Route path="/"  element={<Home />} />
          <Route path="/explorer"  element={<Explorer />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        </Layout>
   
  );
};

export default App;


