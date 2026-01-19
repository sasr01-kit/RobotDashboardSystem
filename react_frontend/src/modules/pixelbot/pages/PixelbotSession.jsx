import { useParams } from "react-router-dom";

export default function PixelbotSession() {
  const { sessionId } = useParams();
  return (
    <div style={{ padding: 24 }}>
      <h1>Session Detail</h1>
      <p>Session ID: {sessionId}</p>
      <p>[Drawing/Transcript/Story summary placeholders]</p>
    </div>
  );
}