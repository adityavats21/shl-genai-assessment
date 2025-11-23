import axios from "axios";

const BASE =
  import.meta.env.VITE_API_URL ||
  "https://shl-genai-assessment.onrender.com";

export async function getRecommendations(query) {
  const url = `${BASE.replace(/\/+$/, "")}/recommend`;
  const resp = await axios.post(url, { query });
  return resp.data;
}
