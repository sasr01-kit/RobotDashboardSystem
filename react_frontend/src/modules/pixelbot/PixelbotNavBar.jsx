import { useLocation, useNavigate } from "react-router-dom";
import { useMemo, useRef, useEffect, useState } from "react";
import "./Pixelbot.css";

export default function PixelbotNavBar() {
  const navigate = useNavigate();
  const location = useLocation();

  const isChildRoute = location.pathname.includes("/pixelbot/child/");
  const [menuOpen, setMenuOpen] = useState(false);
  const [selectedChildId, setSelectedChildId] = useState(""); // IMPORTANT: empty by default

  const menuRef = useRef(null);

  const children = useMemo(
    () => [
      { id: "123", name: "Child A", sessions: ["s1", "s2", "s3"] },
      { id: "456", name: "Child B", sessions: ["s1", "s2"] },
    ],
    []
  );

  const selectedChild = children.find((c) => c.id === selectedChildId);

  useEffect(() => {
    function handleClickOutside(e) {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <nav
      className="pixelbot-navbar"
      data-active={isChildRoute ? "child" : "summary"}
    >
      <div className="tab-strip">
        <button
          type="button"
          className="tab-button summary-tab"
          onClick={() => {
            setMenuOpen(false);
            setSelectedChildId(""); // reset selection when going summary
            navigate("/pixelbot");
          }}
        >
          Summary
        </button>

        <div className="child-menu" ref={menuRef}>
          <button
            type="button"
            className="tab-button child-tab"
            aria-expanded={menuOpen}
            onClick={() => {
              setMenuOpen((v) => !v);
              setSelectedChildId(""); // IMPORTANT: open list-only first
            }}
          >
            Child ▾
          </button>

          {menuOpen && (
            <div className="child-menu-panel child-menu-panel--wide">
              <div className="child-list">
                {children.map((c) => (
                  <button
                    key={c.id}
                    type="button"
                    className="child-list-item"
                    onClick={() => setSelectedChildId(c.id)}
                  >
                    {c.name}
                  </button>
                ))}
              </div>

              {/* Only render right panel AFTER selecting a child */}
              {selectedChild && (
                <div className="child-actions-panel">
                  <button
                    type="button"
                    className="child-action-btn recap"
                    onClick={() => {
                      setMenuOpen(false);
                      navigate(`/pixelbot/child/${selectedChild.id}`);
                    }}
                  >
                    Recap
                  </button>

                  <div className="session-grid">
                    {selectedChild.sessions.map((s) => (
                      <button
                        key={s}
                        type="button"
                        className="child-action-btn session"
                        onClick={() => {
                          setMenuOpen(false);
                          navigate(
                            `/pixelbot/child/${selectedChild.id}/session/${s}`
                          );
                        }}
                      >
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="tab-underline" />
      </div>
    </nav>
  );
}