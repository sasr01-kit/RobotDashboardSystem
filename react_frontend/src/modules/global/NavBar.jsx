import './NavBar.css';

/*
  Generic horizontal navigation bar
  - tabs: [{ label: string, value: string }]
  - active: string (value of currently active tab)
  - onSelect: (value: string) => void
  - isDisabled?: (value: string) => boolean
*/
export default function NavBar({ tabs, active, onSelect, isDisabled }) {
  return (
    <nav className="nav-bar" role="tablist" aria-label="Section Navigation">
      {tabs.map(({ label, value }) => {
        const disabled = isDisabled ? isDisabled(value) : false;
        const isActive = active === value;
        return (
          <button
            key={value}
            role="tab"
            aria-selected={isActive}
            aria-disabled={disabled}
            className={`nav-tab${isActive ? ' active' : ''}${disabled ? ' disabled' : ''}`}
            onClick={() => !disabled && onSelect && onSelect(value)}
            disabled={disabled}
            type="button"
          >
            {label}
          </button>
        );
      })}
    </nav>
  );
}
