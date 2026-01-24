import StatCard from "../components/StatCard";
import PixelbotTopBar from "../components/PixelbotTopBar";
// import kitLogo from "../assets/kit-logo.png"; // varsa aç

export default function PixelbotSummary() {
  const stats = {
    totalSessions: 315,
    sessionsPerDay: 10,
    sessionsPerChild: 8,
  };

  const childrenList = [
    { id: "123", name: "Child A" },
    { id: "456", name: "Child B" },
    { id: "789", name: "Child C" },
  ];

  return (
    <div
      style={{
        background: "var(--bg-light)",
        minHeight: "100vh",
        padding: "24px 24px 60px",
        color: "var(--kit-blue)",
      }}
    >
      {/* =========================
          HEADER (LEFT-ALIGNED)
         ========================= */}
      <div
        style={{
          maxWidth: 1400,
          paddingLeft: 12,
          paddingRight: 12,
          margin: 0, // left aligned
        }}
      >
     

        {/* Tabs row (Summary | Child ▾) */}
        <PixelbotTopBar childrenList={childrenList} />
      </div>

      {/* =========================
          CONTENT (CENTERED BLOCK)
         ========================= */}
      <div
        style={{
          maxWidth: 1180,
          margin: "18px auto 0",
          paddingLeft: 12,
          paddingRight: 12,
        }}
      >
        {/* Stat cards row */}
        <div
          className="pb-3col"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: 18,
            marginBottom: 22,
            alignItems: "stretch",
          }}
        >
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

        {/* Robot usage history */}
        <section
          style={{
            background: "white",
            borderRadius: 14,
            border: "1px solid rgba(0,0,0,0.10)",
            padding: 18,
          }}
        >
          {/* Title + print icon inside card */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              marginBottom: 12,
            }}
          >
            <div style={{ fontWeight: 800 }}>Robot Usage History</div>

            <button
              type="button"
              onClick={() => window.print()}
              title="Print / Export"
              style={{
                width: 34,
                height: 34,
                borderRadius: 10,
                border: "1px solid rgba(0,0,0,0.12)",
                background: "white",
                cursor: "pointer",
                display: "grid",
                placeItems: "center",
                padding: 0,
              }}
            >
              <span style={{ fontSize: 16 }}>🖨️</span>
            </button>
          </div>

          {/* Heatmap placeholder */}
          <div
            style={{
              borderRadius: 12,
              border: "1px dashed rgba(0,0,0,0.18)",
              background: "var(--bg-light)",
              height: 260,
              display: "grid",
              placeItems: "center",
              color: "rgba(0,0,0,0.55)",
              marginTop: 12,
            }}
          >
            [Heatmap placeholder]
          </div>

          <div style={{ marginTop: 10, fontSize: 11, opacity: 0.6 }}>
            Mockup graph from https://github.com/highcharts
          </div>
        </section>

        {/* Responsive */}
        <style>{`
          @media (max-width: 900px) {
            .pb-3col { grid-template-columns: 1fr !important; }
          }
        `}</style>
      </div>
    </div>
  );
}