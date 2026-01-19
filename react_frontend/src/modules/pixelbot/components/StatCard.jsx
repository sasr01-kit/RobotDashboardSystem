export default function StatCard({ title, value, subtitle, variant = "light" }) {
    const variants = {
      green: {
        background: "var(--kit-green)",
        color: "white",
        border: "1px solid rgba(0,0,0,0.06)",
      },
      blue: {
        background: "var(--kit-blue)",
        color: "white",
        border: "1px solid rgba(0,0,0,0.06)",
      },
      light: {
        background: "white",
        color: "var(--kit-blue)",
        border: "1px solid rgba(0,0,0,0.10)",
      },
    };
  
    const v = variants[variant] ?? variants.light;
  
    return (
      <div
        style={{
          border: v.border,
          borderRadius: 14,
          padding: 18,
          minWidth: 220,
          background: v.background,
          color: v.color,
        }}
      >
        <div style={{ fontSize: 14, opacity: 0.9, fontWeight: 700 }}>
          {title}
        </div>
  
        <div style={{ fontSize: 34, fontWeight: 800, marginTop: 10 }}>
          {value}
        </div>
  
        {subtitle ? (
          <div style={{ fontSize: 12, opacity: 0.85, marginTop: 10 }}>
            {subtitle}
          </div>
        ) : null}
      </div>
    );
  }