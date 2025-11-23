#!/bin/bash

PROJECT="shl-frontend"
API_URL="https://shl-genai-assessment.onrender.com"

echo "📁 Creating Next.js + Tailwind project..."

npx create-next-app@latest $PROJECT --typescript --eslint --tailwind --app --no-src-dir --use-npm

cd $PROJECT

# Create API environment variable
echo "NEXT_PUBLIC_API_URL=$API_URL" > .env.local

# Create UI page
cat > app/page.tsx << 'EOF'
"use client";
import { useState } from "react";

export default function HomePage() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  async function fetchResults() {
    setLoading(true);
    try {
      const res = await fetch(
        process.env.NEXT_PUBLIC_API_URL + "/recommend",
        {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({ query }),
        }
      );

      const data = await res.json();
      setResults(data.recommended_assessments || []);
    } catch (e) {
      console.error(e);
      alert("API error");
    }
    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-gray-50 p-10">
      <h1 className="text-4xl font-bold text-center mb-6">
        SHL Assessment Recommender
      </h1>

      <textarea
        className="w-full border p-4 rounded-md"
        placeholder="Paste job description here…"
        rows={6}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button
        onClick={fetchResults}
        className="bg-indigo-600 text-white px-6 py-3 rounded-lg mt-4"
      >
        {loading ? "Loading..." : "Recommend"}
      </button>

      <div className="mt-10 space-y-5">
        {results.map((item, i) => (
          <div key={i} className="p-6 bg-white rounded-lg shadow">
            <h2 className="text-xl font-semibold">{item.name}</h2>
            <p className="mt-2">{item.description}</p>
            <a
              href={item.url}
              target="_blank"
              className="text-indigo-600 underline mt-2 inline-block"
            >
              View Assessment →
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
EOF

echo "🎉 Frontend created successfully!"
echo "👉 Run locally: cd $PROJECT && npm run dev"
echo "👉 Deploy to Vercel: vercel --prod"


