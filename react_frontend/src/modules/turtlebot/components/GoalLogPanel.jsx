import { useRef } from 'react';
import { useTurtlebotGoal } from '../Hooks/useTurtlebotGoal';
import { useTurtlebotGoalMock } from '../Hooks/useTurtlebotGoalMock'; //MOCK DELETE
import { GoalEntryBlock } from './GoalEntryBlock';
import { PathLogDropdownNav } from './PathLogDropdownNav';
import { motion } from 'framer-motion';

export const GoalLogPanel = ({ logs, entryRefs }) => {

  return (
    <motion.div 
      className="goal-log-panel"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
        {logs.length === 0 ? (
          <div className="empty-log">No goal logs yet.</div>
        ) : (
          logs.map((log) => (
            <div key={log.id} ref={(element) => (entryRefs.current[log.id] = element)}
            >
              <GoalEntryBlock log={log} />
            </div>
        ))
      )}
    </motion.div>
  );
};

