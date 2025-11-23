import React, { useState } from "react";
import Header from "./components/Header";
import { getRecommendations } from "./api/recommend";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [items, setItems] = useState([]);

  const [text, setText] = useState("");

  const handleSearch = async () => {
    if (!text.trim()) return;

    setLoading(true);
    const res = await getRecommendations(text);
    setItems(res || []);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <Header />

      <div className="max-w-3xl mx-auto px-6 mt-14">
        <div className="bg-white/40 backdrop-blur-xl shadow-xl rounded-2xl p-8 border border-white/20">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            Job Description
          </h2>

          <textarea
            className="w-full h-40 p-4 rounded-xl border border-gray-300 focus:ring-4 focus:ring-blue-200 outline-none shadow-sm text-gray-700"
            placeholder="Paste job description…"
            onChange={(e) => setText(e.target.value)}
          />

          <button
            onClick={handleSearch}
            className="mt-6 w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-700 transition-all text-white font-semibold shadow-lg"
          >
            {loading ? "Loading..." : "Get Recommendations"}
          </button>
        </div>

        {/* Results */}
        <div className="mt-10">
          {loading ? (
            <p className="text-center text-gray-500">Analyzing…</p>
          ) : items.length === 0 ? (
            <p className="text-center text-gray-500">
              No recommendations yet.
            </p>
          ) : (
            <div className="grid gap-4 mt-4">
              {items.map((item, idx) => (
                <div
                  key={idx}
                  className="p-6 rounded-xl bg-white shadow-md border border-gray-200 hover:shadow-xl transition-all"
                >
                  <h4 className="text-xl font-semibold text-gray-900">
                    {item.name}
                  </h4>
                  <p className="text-gray-600 mt-2">{item.description}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
