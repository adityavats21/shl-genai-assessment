import React, { useState } from "react";

export default function SearchSection({ onSearch, loading }) {
  const [text, setText] = useState("");

  const submit = () => {
    if (!text.trim()) return;
    onSearch(text);
  };

  return (
    <div className="max-w-3xl mx-auto mt-12 glass p-8">
      <h2 className="text-xl font-semibold mb-4">Enter Job Description</h2>

      <textarea
        className="w-full h-32 p-4 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none"
        placeholder="Paste job description..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        onClick={submit}
        disabled={loading}
        className="mt-4 w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
      >
        {loading ? "Processing..." : "Get Recommendations"}
      </button>
    </div>
  );
}
