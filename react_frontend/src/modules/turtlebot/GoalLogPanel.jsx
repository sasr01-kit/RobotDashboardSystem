import { useRef } from 'react';
import { useTurtlebotGoal } from './Hooks/useTurtlebotGoal';
import { useTurtlebotGoalMock } from './Hooks/useTurtlebotGoalMock'; //MOCK DELETE
import { GoalEntryBlock } from './GoalEntryBlock';
import { PathLogDropdownNav } from './PathLogDropdownNav';

export const GoalLogPanel = ({ logs, entryRefs }) => {

  return (
    <div className="goal-log-panel">
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
    </div>
  );
};

