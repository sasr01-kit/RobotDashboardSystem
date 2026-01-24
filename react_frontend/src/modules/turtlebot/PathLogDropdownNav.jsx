import { useState } from 'react';

export const PathLogDropdownNav = ({ logs, onSelect }) => {
    const [isOpen, setIsOpen] = useState(false);

    const handleSelect = (id) => {
        onSelect(id);
        setIsOpen(false);
    }
  
    return (
    <div className="path-log-dropdown-nav">
      <div className={`dropdown-label ${isOpen ? "open" : ""}`}
      onClick={() => setIsOpen((prev) => !prev)}
      >
        Path History <span className="triangle">▼</span>
      </div>

      {isOpen && (
        <ul className="dropdown-menu">
          {logs.map((log) => (
            <li key={log.id} onClick={() => handleSelect(log.id)}>
              {log.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
