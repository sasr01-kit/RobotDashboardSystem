import { useParams } from "react-router-dom";
import DashboardCard from "../reusableComponents/DashboardCard";
import ImageCarousel from "../reusableComponents/ImageCarousel";
import BarChart from "../reusableComponents/BarChart";
import StackedBarChart from "../reusableComponents/StackedBarChart";

export default function PixelbotChildRecap() {
  const { childId } = useParams();
  const drawingImages = [
    "https://picsum.photos/seed/pixelbot-drawing-1/480/280",
    "https://picsum.photos/seed/pixelbot-drawing-2/480/280",
    "https://picsum.photos/seed/pixelbot-drawing-3/480/280",
  ];
  // Backend session metrics will be mapped into { label, value } for the chart.
  const wordCountData = [
    { label: "S1", value: 1200 },
    { label: "S2", value: 1800 },
    { label: "S3", value: 1500 },
  ];
  // TODO (backend):
  // Replace this mock data with real backend response.
  // Backend should return, per color, a list of segment entries
  // where each entry represents one session's usage count.
  // The data must be mapped into:
  // Map<ColorName, SegmentEntry[]>
  const colorsUsedData = new Map([
    [
      "Red",
      [
        { label: "Session 1", value: 12 },
        { label: "Session 2", value: 2 },
        { label: "Session 3", value: 6 },
      ],
    ],
    [
      "Blue",
      [
        { label: "Session 1", value: 2 },
        { label: "Session 2", value: 14 },
        { label: "Session 3", value: 16 },
      ],
    ],
    [
      "Yellow",
      [
        { label: "Session 1", value: 14 },
        { label: "Session 2", value: 8 },
        { label: "Session 3", value: 6 },
      ],
    ],
  ]);
  // Limit to the last 3 sessions for readability and UX.
  const colorsUsedLastSessions = new Map(
    Array.from(colorsUsedData.entries()).map(([color, segments]) => [
      color,
      segments.slice(-3),
    ])
  );
  return (
    <div className="pb-content">
      <h1>Child {childId} – Recap</h1>
      <div className="pb-recap-grid">
        <div className="pb-recap-col">
          <DashboardCard title="Drawing(s)">
            <ImageCarousel images={drawingImages} />
          </DashboardCard>
          <DashboardCard title="Speech Time">
            <div className="pb-heatmap">[Speech time chart placeholder]</div>
          </DashboardCard>
        </div>
        <div className="pb-recap-col">
          <DashboardCard title="Word Count">
            <BarChart
              data={wordCountData}
              xAxisLabel="Sessions"
              yAxisLabel="Words"
              ariaLabel="Word count by session"
            />
          </DashboardCard>
          <DashboardCard title="Colors Used">
            <StackedBarChart
              data={colorsUsedLastSessions}
              orientation="horizontal"
              ariaLabel="Colors used per session"
            />
          </DashboardCard>
        </div>
        <div className="pb-recap-col">
          <div className="pb-card pb-kpi">
            <div className="pb-card-title">Total Sessions</div>
            <div>16</div>
            <div className="pb-kpi-sub">+3 than last month</div>
          </div>
          <div className="pb-card pb-kpi">
            <div className="pb-card-title">Total Word Count</div>
            <div>13 450</div>
            <div className="pb-kpi-sub">-200 than last month</div>
          </div>
          <div className="pb-card pb-kpi">
            <div className="pb-card-title">Average Intimacy Score</div>
            <div>70%</div>
            <div className="pb-kpi-sub">+10% than last month</div>
          </div>
        </div>
      </div>
    </div>
  );
}
