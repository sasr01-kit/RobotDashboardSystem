import { useState } from 'react';
import { motion } from 'framer-motion';

export const PathLogDropdownNav = ({ logs, onSelect }) => {
    const [isOpen, setIsOpen] = useState(false);

    const handleSelect = (id) => {
        onSelect(id);
        setIsOpen(false);
    }
  
    return (
    <motion.div 
      className="path-log-dropdown-nav"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className={`dropdown-label ${isOpen ? "open" : ""}`}
      onClick={() => setIsOpen((prev) => !prev)}
      >
        Path History <span className="triangle">▼</span>
      </div>

      {isOpen && (
        <ul className="dropdown-menu">
          {logs.map((log) => (
            <li key={log.id} onClick={() => handleSelect(log.id)}>
              {log.goalType} - {new Date(log.timestamp).toLocaleString()}
            </li>
          ))}
        </ul>
      )}
    </motion.div>
  );
};
