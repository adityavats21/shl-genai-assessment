mkdir -p public src/components src/api src/assets

cat << 'EOT' > package.json
{
  "name": "shl-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "start": "craco start",
    "build": "craco build",
    "test": "craco test"
  },
  "dependencies": {
    "axios": "^1.4.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "devDependencies": {
    "@craco/craco": "^7.0.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.24",
    "tailwindcss": "^3.4.8"
  }
}
EOT

cat << 'EOT' > tailwind.config.js
module.exports = {
  content: ["./src/**/*.{js,jsx}", "./public/index.html"],
  theme: {
    extend: {
      colors: {
        brand: {50:"#f5fbff",100:"#e6f5ff",500:"#0b74ff",700:"#075bb5"}
      }
    }
  },
  plugins: []
}
EOT

cat << 'EOT' > postcss.config.js
module.exports = { plugins: { tailwindcss:{}, autoprefixer:{} } };
EOT

cat << 'EOT' > craco.config.js
module.exports = {
  style: { postcss: { plugins: [require('tailwindcss'), require('autoprefixer')] } }
};
EOT

cat << 'EOT' > public/index.html
<!DOCTYPE html>
<html><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/></head>
<body><div id="root"></div></body></html>
EOT

cat << 'EOT' > src/main.css
@tailwind base;
@tailwind components;
@tailwind utilities;
body { @apply bg-gray-50 text-gray-800; }
EOT

cat << 'EOT' > src/index.jsx
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./main.css";
createRoot(document.getElementById("root")).render(<App />);
EOT

cat << 'EOT' > src/api/recommend.js
import axios from "axios";
const BASE = process.env.REACT_APP_API_URL || "https://YOUR_BACKEND_URL";
export async function getRecommendations(query) {
  const url = \`\${BASE.replace(/\/+$/, "")}/recommend\`;
  const resp = await axios.post(url, { query });
  return resp.data;
}
EOT

cat << 'EOT' > src/components/Header.jsx
import React from "react";
import logo from "../assets/logo.svg";
export default function Header() {
  return (
    <header className="bg-white shadow-sm p-4 flex gap-3 items-center">
      <img src={logo} className="h-10 w-10"/>
      <div>
        <h1 className="text-lg font-semibold">SHL Assessment Recommender</h1>
        <p className="text-sm text-gray-500">Query any JD</p>
      </div>
    </header>
  );
}
EOT

cat << 'EOT' > src/components/SearchBar.jsx
import React, { useState } from "react";

export default function SearchBar({ onSearch, loading }) {
  const [q, setQ] = useState("");
  return (
    <form onSubmit={(e)=>{e.preventDefault();onSearch(q);}} className="p-4">
      <textarea className="border p-3 w-full rounded" rows="3"
        value={q} onChange={(e)=>setQ(e.target.value)}
        placeholder="Paste job description or query"
      />
      <button className="mt-3 px-4 py-2 bg-brand-500 text-white rounded">
        {loading ? "Loading..." : "Search"}
      </button>
    </form>
  );
}
EOT

cat << 'EOT' > src/components/ResultsTable.jsx
import React from "react";
export default function ResultsTable({ recommendations=[] }) {
  if (!recommendations.length) return <div className="p-6 text-center text-gray-500">No results.</div>;
  return (
    <table className="w-full bg-white shadow rounded mt-4">
      <thead><tr><th className="p-3 text-left">Name</th><th className="p-3 text-left">Description</th><th className="p-3">URL</th></tr></thead>
      <tbody>
        {recommendations.map((r,i)=>(
          <tr key={i} className="border-t">
            <td className="p-3">{r.name}</td>
            <td className="p-3">{r.description}</td>
            <td className="p-3"><a className="text-brand-500 underline" href={r.url}>Open</a></td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
EOT

cat << 'EOT' > src/components/Spinner.jsx
import React from "react";
export default function Spinner(){return <div className="p-6 text-center animate-pulse">Loading...</div>;}
EOT

cat << 'EOT' > src/assets/logo.svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#0b74ff"/><text x="50" y="58" text-anchor="middle" font-size="36" fill="white" font-family="sans-serif" font-weight="700">SHL</text></svg>
EOT

cat << 'EOT' > src/App.jsx
import React, { useState } from "react";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import ResultsTable from "./components/ResultsTable";
import Spinner from "./components/Spinner";
import { getRecommendations } from "./api/recommend";

export default function App(){
  const [data,setData]=useState([]);
  const [loading,setLoading]=useState(false);

  async function search(q){
    setLoading(true);
    const res = await getRecommendations(q);
    setData(res.recommended_assessments || []);
    setLoading(false);
  }

  return (
    <div>
      <Header/>
      <SearchBar onSearch={search} loading={loading}/>
      {loading ? <Spinner/> : <ResultsTable recommendations={data}/>}
    </div>
  );
}
EOT
