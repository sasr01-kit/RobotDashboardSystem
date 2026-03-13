import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import TurtlebotStatusPage from '../../modules/turtlebot/pages/TurtlebotStatusPage.jsx'

vi.mock('../../modules/turtlebot/hooks/useTurtlebotStatus.js', () => ({
  useTurtlebotStatus: vi.fn(),
}))

vi.mock('../../modules/turtlebot/components/PowerStatus.jsx', () => ({
  default: ({ isOn }) => <div>PowerStatus:{String(isOn)}</div>,
}))

vi.mock('../../modules/turtlebot/components/ModeStatus.jsx', () => ({
  default: () => <div>ModeStatus</div>,
}))

vi.mock('../../modules/turtlebot/components/TeleoperationBlock.jsx', () => ({
  default: () => <div>TeleoperationBlock</div>,
}))

vi.mock('../../modules/turtlebot/components/PathExecutionBlock.jsx', () => ({
  default: () => <div>PathExecutionBlock</div>,
}))

vi.mock('../../modules/turtlebot/components/DockingBlock.jsx', () => ({
  default: () => <div>DockingBlock</div>,
}))

vi.mock('../../modules/turtlebot/components/GeneralStatusBlock.jsx', () => ({
  default: ({ label, status, statusClass }) => (
    <div>
      <span>{label}</span>
      <span>{String(status)}</span>
      <span>{statusClass}</span>
    </div>
  ),
}))

import { useTurtlebotStatus } from '../../modules/turtlebot/hooks/useTurtlebotStatus.js'

describe('TurtlebotStatusPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the main status page blocks', () => {
    useTurtlebotStatus.mockReturnValue({
      error: null,
      statusDTO: {
        isOn: true,
        batteryPercentage: 70,
        isWifiConnected: true,
        isCommsConnected: true,
        isRaspberryPiConnected: true,
        mode: 'Teleoperating',
        isDocked: false,
      },
    })

    render(<TurtlebotStatusPage />)

    expect(screen.getByText('PowerStatus:true')).toBeInTheDocument()
    expect(screen.getByText('ModeStatus')).toBeInTheDocument()
    expect(screen.getByText('TeleoperationBlock')).toBeInTheDocument()
    expect(screen.getByText('PathExecutionBlock')).toBeInTheDocument()
    expect(screen.getByText('DockingBlock')).toBeInTheDocument()

    expect(screen.getByText('Battery')).toBeInTheDocument()
    expect(screen.getByText('70%')).toBeInTheDocument()
    expect(screen.getByText('status-high-battery')).toBeInTheDocument()

    expect(screen.getByText('WiFi')).toBeInTheDocument()
    expect(screen.getAllByText('Connected').length).toBeGreaterThan(0)
    expect(screen.getAllByText('status-connected').length).toBeGreaterThan(0)
  })

  it('renders low battery class when battery is below 50', () => {
    useTurtlebotStatus.mockReturnValue({
      error: null,
      statusDTO: {
        isOn: true,
        batteryPercentage: 20,
        isWifiConnected: false,
        isCommsConnected: false,
        isRaspberryPiConnected: false,
        mode: 'Teleoperating',
        isDocked: false,
      },
    })

    render(<TurtlebotStatusPage />)

    expect(screen.getByText('20%')).toBeInTheDocument()
    expect(screen.getByText('status-low-battery')).toBeInTheDocument()
    expect(screen.getAllByText('status-disconnected').length).toBeGreaterThan(0)
  })

  it('renders disconnected battery class when battery percentage is null', () => {
    useTurtlebotStatus.mockReturnValue({
      error: null,
      statusDTO: {
        isOn: false,
        batteryPercentage: null,
        isWifiConnected: false,
        isCommsConnected: false,
        isRaspberryPiConnected: false,
        mode: 'Teleoperating',
        isDocked: false,
      },
    })

    render(<TurtlebotStatusPage />)

    expect(screen.getByText('null%')).toBeInTheDocument()
    expect(screen.getAllByText('status-disconnected').length).toBeGreaterThan(0)
  })

  it('renders error page when hook returns an error', () => {
    useTurtlebotStatus.mockReturnValue({
      error: 'Failed to parse Turtlebot status',
      statusDTO: null,
    })

    render(<TurtlebotStatusPage />)

    expect(screen.getByText('Error: Failed to parse Turtlebot status')).toBeInTheDocument()
  })
})