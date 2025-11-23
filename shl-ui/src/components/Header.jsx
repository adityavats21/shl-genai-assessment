import React from "react";

export default function Header() {
  return (
    <header className="w-full bg-gradient-to-r from-blue-600 to-blue-500 shadow-lg">
      <div className="max-w-7xl mx-auto px-6 py-5 flex items-center gap-4">
        <div className="w-12 h-12 rounded-xl bg-white/20 backdrop-blur-lg flex items-center justify-center text-white font-bold text-xl shadow-inner">
          SHL
        </div>

        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">
            SHL Assessment Recommender
          </h1>
          <p className="text-blue-100 text-sm tracking-wide">
            AI-assisted hiring recommendations
          </p>
        </div>
      </div>
    </header>
  );
}
