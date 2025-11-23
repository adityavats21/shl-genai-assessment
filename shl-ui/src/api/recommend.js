import axios from "axios";

const API_BASE = "https://shl-genai-assessment.onrender.com"; 

export async function getRecommendations(query) {
  try {
    const response = await axios.post(`${API_BASE}/recommend`, {
      query: query,   
    });

    return response.data.recommended_assessments;

  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}
