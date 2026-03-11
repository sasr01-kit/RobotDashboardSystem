import React from 'react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import TurtlebotMapPage from '../../modules/turtlebot/pages/TurtlebotMapPage.jsx'

const saveMock = vi.fn()
const loadLatestMock = vi.fn()
const clearMock = vi.fn()
const scrollIntoViewMock = vi.fn()

vi.mock('../../modules/turtlebot/hooks/useTurtlebotGoal.js', () => ({
  useTurtlebotGoal: vi.fn(),
  usePathHistoryActions: vi.fn(),
}))

vi.mock('../../modules/turtlebot/components/GoalLogPanel.jsx', () => ({
  GoalLogPanel: ({ logs, entryRefs }) => (
    <div data-testid="goal-log-panel">
      logs:{logs.length}
      {logs.map((log) => (
        <div
          key={log.id}
          data-testid={`goal-entry-${log.id}`}
          ref={(el) => {
            if (el) {
              entryRefs.current[log.id] = el
            }
          }}
        >
          {log.label}
        </div>
      ))}
    </div>
  ),
}))

vi.mock('../../modules/turtlebot/components/PathLogDropdownNav.jsx', () => ({
  PathLogDropdownNav: ({ logs, onSelect }) => (
    <div data-testid="path-log-dropdown">
      dropdown:{logs.length}
      <button onClick={() => onSelect('1')}>Select Entry 1</button>
      <button onClick={() => onSelect('missing')}>Select Missing Entry</button>
    </div>
  ),
}))

vi.mock('../../modules/turtlebot/components/MinimizedStatusBar.jsx', () => ({
  MinimizedStatusBar: () => (
    <div data-testid="minimized-status-bar">MinimizedStatusBar</div>
  ),
}))

vi.mock('../../modules/turtlebot/components/MapView.jsx', () => ({
  default: ({ onMapResize }) => {
    React.useEffect(() => {
      onMapResize(500)
    }, [onMapResize])

    return <div data-testid="map-view">MapView</div>
  },
}))

vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, initial, animate, exit, transition, whileHover, whileTap, ...props }) => (
      <div {...props}>{children}</div>
    ),
    button: ({ children, initial, animate, exit, transition, whileHover, whileTap, ...props }) => (
      <button {...props}>{children}</button>
    ),
  },
  AnimatePresence: ({ children }) => <>{children}</>,
}))

import {
  useTurtlebotGoal,
  usePathHistoryActions,
} from '../../modules/turtlebot/hooks/useTurtlebotGoal.js'

describe('TurtlebotMapPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    scrollIntoViewMock.mockReset()
    Element.prototype.scrollIntoView = scrollIntoViewMock

    usePathHistoryActions.mockReturnValue({
      save: saveMock,
      loadLatest: loadLatestMock,
      clear: clearMock,
    })
  })

  it('renders map page sections with path history', () => {
    useTurtlebotGoal.mockReturnValue({
      pathHistory: [
        { id: '1', label: 'Goal A' },
        { id: '2', label: 'Goal B' },
      ],
    })

    render(<TurtlebotMapPage />)

    expect(screen.getByTestId('minimized-status-bar')).toBeInTheDocument()
    expect(screen.getByTestId('map-view')).toBeInTheDocument()
    expect(screen.getByTestId('path-log-dropdown')).toHaveTextContent('dropdown:2')
    expect(screen.getByTestId('goal-log-panel')).toHaveTextContent('logs:2')
    expect(screen.getByText('Save')).toBeInTheDocument()
    expect(screen.getByText('Load')).toBeInTheDocument()
    expect(screen.getByText('Clear')).toBeInTheDocument()
  })

  it('calls save when Save is clicked', () => {
    useTurtlebotGoal.mockReturnValue({
      pathHistory: [{ id: '1', label: 'Goal A' }],
    })

    render(<TurtlebotMapPage />)

    fireEvent.click(screen.getByText('Save'))
    expect(saveMock).toHaveBeenCalled()
  })

  it('calls loadLatest when Load is clicked', () => {
    useTurtlebotGoal.mockReturnValue({
      pathHistory: [{ id: '1', label: 'Goal A' }],
    })

    render(<TurtlebotMapPage />)

    fireEvent.click(screen.getByText('Load'))
    expect(loadLatestMock).toHaveBeenCalled()
  })

  it('disables Clear when there is no path history', () => {
    useTurtlebotGoal.mockReturnValue({
      pathHistory: [],
    })

    render(<TurtlebotMapPage />)

    expect(screen.getByText('Clear')).toBeDisabled()
  })

  it('opens confirmation modal when Clear is clicked', () => {
    useTurtlebotGoal.mockReturnValue({
      pathHistory: [{ id: '1', label: 'Goal A' }],
    })

    render(<TurtlebotMapPage />)

    fireEvent.click(screen.getByText('Clear'))

    expect(screen.getByText('Clear current path history?')).toBeInTheDocument()
    expect(screen.getByText('Cancel')).toBeInTheDocument()
    expect(screen.getByText('Clear history')).toBeInTheDocument()
  })

  it('closes confirmation modal when Cancel is clicked', () => {
    useTurtlebotGoal.mockReturnValue({
      pathHistory: [{ id: '1', label: 'Goal A' }],
    })

    render(<TurtlebotMapPage />)

    fireEvent.click(screen.getByText('Clear'))
    fireEvent.click(screen.getByText('Cancel'))

    expect(screen.queryByText('Clear current path history?')).not.toBeInTheDocument()
  })

  it('closes confirmation modal when backdrop is clicked', () => {
    useTurtlebotGoal.mockReturnValue({
      pathHistory: [{ id: '1', label: 'Goal A' }],
    })

    const { container } = render(<TurtlebotMapPage />)

    fireEvent.click(screen.getByText('Clear'))
    expect(screen.getByText('Clear current path history?')).toBeInTheDocument()

    const backdrop = container.querySelector('.confirm-modal-backdrop')
    fireEvent.click(backdrop)

    expect(screen.queryByText('Clear current path history?')).not.toBeInTheDocument()
  })

  it('calls clear and closes modal when Clear history is confirmed', () => {
    useTurtlebotGoal.mockReturnValue({
      pathHistory: [{ id: '1', label: 'Goal A' }],
    })

    render(<TurtlebotMapPage />)

    fireEvent.click(screen.getByText('Clear'))
    fireEvent.click(screen.getByText('Clear history'))

    expect(clearMock).toHaveBeenCalled()
    expect(screen.queryByText('Clear current path history?')).not.toBeInTheDocument()
  })

  it('scrolls to the selected entry when chosen from the dropdown', () => {
    useTurtlebotGoal.mockReturnValue({
      pathHistory: [{ id: '1', label: 'Goal A' }],
    })

    render(<TurtlebotMapPage />)

    fireEvent.click(screen.getByText('Select Entry 1'))

    expect(scrollIntoViewMock).toHaveBeenCalledWith({
      behavior: 'smooth',
      block: 'nearest',
    })
  })

  it('does nothing when selecting an entry that does not exist', () => {
    useTurtlebotGoal.mockReturnValue({
      pathHistory: [{ id: '1', label: 'Goal A' }],
    })

    render(<TurtlebotMapPage />)

    fireEvent.click(screen.getByText('Select Missing Entry'))

    expect(scrollIntoViewMock).not.toHaveBeenCalled()
  })
})