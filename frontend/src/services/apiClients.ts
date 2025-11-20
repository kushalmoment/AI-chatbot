import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:5000",
});

export async function sendMessage(userId: string, message: string): Promise<string> {
  const token = localStorage.getItem("idToken");
  const resp = await api.post(
    "/api/chat/message",
    { userId, message },
    {
      headers: {
        Authorization: token ? `Bearer ${token}` : "",
      },
    }
  );
  return resp.data.reply;
}
