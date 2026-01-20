import StatCard from "../reusableComponents/StatCard";

export default function PixelbotSummary() {
  const stats = {
    totalSessions: 315,
    sessionsPerDay: 10,
    sessionsPerChild: 8,
  };

  return (
    <div className="pb-content">
      <div className="pb-3col">
        <StatCard
          title="Total Session"
          value={stats.totalSessions}
          subtitle="Total Sessions for the month"
          variant="green"
        />
        <StatCard
          title="Sessions per day"
          value={stats.sessionsPerDay}
          subtitle="Average robot session per day for a month"
          variant="blue"
        />
        <StatCard
          title="Sessions per child"
          value={stats.sessionsPerChild}
          subtitle="Average session a child has per month"
          variant="light"
        />
      </div>

      <section className="pb-card">
        <div className="pb-card-header">
          <div className="pb-card-title">Robot Usage History</div>
          <button
            type="button"
            onClick={() => window.print()}
            title="Print / Export"
            className="pb-icon-btn"
          >
            <span className="pb-icon">🖨️</span>
          </button>
        </div>

        <div className="pb-heatmap">[Heatmap placeholder]</div>

        <div className="pb-footnote">
          Mockup graph from https://github.com/highcharts
        </div>
      </section>
    </div>
  );
}