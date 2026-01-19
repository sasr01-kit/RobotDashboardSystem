import { useParams } from "react-router-dom";

export default function PixelbotChildRecap() {
  const { childId } = useParams();
  return (
    <div style={{ padding: 24 }}>
      <h1>Child Recap</h1>
      <p>Child ID: {childId}</p>
      <p>[Charts/cards placeholder]</p>
    </div>
  );
}