import { Link, useLocation, useNavigate } from "react-router-dom";
import { useMemo, useState } from "react";

export default function PixelbotTopBar({ childrenList = [] }) {
  const location = useLocation();
  const navigate = useNavigate();

  const inChildRoute =
    location.pathname.startsWith("/pixelbot/children") ||
    location.pathname.startsWith("/pixelbot/sessions");

  const [isChildMenuOpen, setIsChildMenuOpen] = useState(false);
  const [activeChildId, setActiveChildId] = useState(childrenList?.[0]?.id ?? null);

  // underline: dropdown açıkken de Child aktif görünsün
  const activeTab = isChildMenuOpen || inChildRoute ? "child" : "summary";

  const sessionsForChild = useMemo(
    () => [
      { id: "S1", name: "Session 1" },
      { id: "S2", name: "Session 2" },
      { id: "S3", name: "Session 3" },
      { id: "S4", name: "Session 4" },
      { id: "S5", name: "Session 5" },
    ],
    []
  );

  const fallbackChildId = childrenList?.[0]?.id ?? "123";

  const tabStyle = (tabName) => ({
    textDecoration: "none",
    fontWeight: 800,
    color: "var(--kit-blue)",
    paddingBottom: 6,
    borderBottom:
      activeTab === tabName
        ? "3px solid var(--kit-green)"
        : "3px solid transparent",
  });

  function goRecap(childId) {
    const id = childId ?? activeChildId ?? fallbackChildId;
    setActiveChildId(id);
    setIsChildMenuOpen(false);
    navigate(`/pixelbot/children/${id}`);
  }

  function selectChild(childId) {
    setActiveChildId(childId);
    // child seçince default recap'e git
    navigate(`/pixelbot/children/${childId}`);
    // menu açık kalsın (figure 5.3 gibi devam etsin)
    setIsChildMenuOpen(true);
  }

  function goSession(sessionId) {
    setIsChildMenuOpen(false);
    navigate(`/pixelbot/sessions/${sessionId}`);
  }

  return (
    <div style={{ position: "relative", marginBottom: 18 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        {/* Summary */}
        <Link to="/pixelbot" style={tabStyle("summary")}>
          Summary
        </Link>

        <div style={{ opacity: 0.35, fontWeight: 700 }}>|</div>

        {/* Child wrapper: hover alanı + dropdown aynı wrapper içinde */}
        <div
          style={{
            position: "relative",
            display: "inline-block",
            // hover gap olmasın diye biraz padding veriyoruz
            paddingBottom: 10,
          }}
          onMouseEnter={() => setIsChildMenuOpen(true)}
          onMouseLeave={() => setIsChildMenuOpen(false)}
        >
          {/* Child tab */}
          <button
            type="button"
            onClick={() => setIsChildMenuOpen((v) => !v)}
            style={{
              all: "unset",
              cursor: "pointer",
              ...tabStyle("child"),
              display: "inline-flex",
              alignItems: "center",
              gap: 6,
            }}
          >
            Child <span style={{ opacity: 0.6, fontSize: 14 }}>▼</span>
          </button>

          {/* Dropdown */}
          {isChildMenuOpen && (
            <div
              style={{
                position: "absolute",
                top: 34,
                left: 0,
                background: "white",
                border: "1px solid rgba(0,0,0,0.10)",
                borderRadius: 14,
                boxShadow: "0 12px 30px rgba(0,0,0,0.12)",
                padding: 12,
                display: "grid",
                gridTemplateColumns: "220px 420px",
                gap: 12,
                zIndex: 999,
              }}
            >
              {/* Left: child list (scrollable yapalım figure gibi) */}
              <div
                style={{
                  display: "grid",
                  gap: 8,
                  maxHeight: 240,
                  overflowY: "auto",
                  paddingRight: 6,
                }}
              >
                {childrenList.map((c) => {
                  const active = c.id === activeChildId;
                  return (
                    <button
                      key={c.id}
                      type="button"
                      onClick={() => selectChild(c.id)}
                      style={{
                        textAlign: "left",
                        padding: "10px 12px",
                        borderRadius: 12,
                        border: active
                          ? "2px solid rgba(0,166,153,0.45)"
                          : "1px solid rgba(0,0,0,0.10)",
                        background: active ? "rgba(0,166,153,0.10)" : "white",
                        cursor: "pointer",
                        fontWeight: 700,
                        fontSize: 14,
                        color: "var(--kit-blue)",
                      }}
                    >
                      {c.name}
                    </button>
                  );
                })}
              </div>

              {/* Right: KIT green panel (Figure 5.3 gibi) */}
              <div
                style={{
                  borderRadius: 14,
                  background: "var(--kit-green)", // ✅ KIT green
                  padding: 12,
                  display: "grid",
                  gap: 10,
                }}
              >
                {/* Recap + sessions: white text */}
                <button
                  type="button"
                  onClick={() => goRecap()}
                  style={{
                    all: "unset",
                    cursor: "pointer",
                    padding: "10px 12px",
                    borderRadius: 12,
                    background: "rgba(255,255,255,0.14)",
                    border: "1px solid rgba(255,255,255,0.22)",
                    color: "white",
                    fontWeight: 800,
                    fontSize: 15,
                    textAlign: "left",
                  }}
                >
                  Recap
                </button>

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
                    gap: 8,
                  }}
                >
                  {sessionsForChild.map((s) => (
                    <button
                      key={s.id}
                      type="button"
                      onClick={() => goSession(s.id)}
                      style={{
                        all: "unset",
                        cursor: "pointer",
                        padding: "10px 12px",
                        borderRadius: 12,
                        background: "rgba(255,255,255,0.14)",
                        border: "1px solid rgba(255,255,255,0.22)",
                        color: "white",
                        fontWeight: 800,
                        fontSize: 14,
                        textAlign: "left",
                      }}
                    >
                      {s.name}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}