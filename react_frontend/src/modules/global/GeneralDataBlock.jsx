import './GeneralDataBlock.css';

/*
  GeneralDataBlock: reusable KPI/status block
  Props:
  - icon: ReactNode
  - label: string
  - status: string | ReactNode
  - statusColor?: CSS color for the value
*/
export default function GeneralDataBlock({ icon, label, status, statusColor }) {
  return (
    <div className="data-block" role="group" aria-label={label}>
      <div className="data-block__icon">{icon}</div>
      <div className="data-block__info">
        <div className="data-block__label">{label}</div>
        <div className="data-block__value" style={{ color: statusColor }}>{status}</div>
      </div>
    </div>
  );
}
