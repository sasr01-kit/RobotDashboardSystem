import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MinimizedStatusBar } from '../../modules/turtlebot/components/MinimizedStatusBar.jsx'
import { useTurtlebotStatus } from '../../modules/turtlebot/hooks/useTurtlebotStatus'
import { getBatteryIcon } from '../../modules/turtlebot/assets/batteryMap'

vi.mock('../../modules/turtlebot/hooks/useTurtlebotStatus', () => ({
  useTurtlebotStatus: vi.fn(),
}))

vi.mock('../../modules/turtlebot/assets/batteryMap', () => ({
  getBatteryIcon: vi.fn(),
}))

// Mocks animations to make testing more focused on functionality and more stable
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, initial, animate, ...props }) => (
      <div {...props}>{children}</div>
    ),
  },
}))

// Tests for MinimizedStatusBar to ensure it renders the correct battery icon and status indicators 
// based on the turtlebot status, and handles missing statusDTO safely
describe('MinimizedStatusBar', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    getBatteryIcon.mockReturnValue('mock-battery-icon.svg')
  })

  it('renders all minimized status indicators with connected/on values', () => {
    useTurtlebotStatus.mockReturnValue({
      statusDTO: {
        isOn: true,
        batteryPercentage: 80,
        isWifiConnected: true,
        isRaspberryPiConnected: true,
        isCommsConnected: true,
      },
    })

    const { container } = render(<MinimizedStatusBar />)

    expect(getBatteryIcon).toHaveBeenCalledWith(80)

    const batteryImg = screen.getByAltText('Battery 80%')
    expect(batteryImg).toBeInTheDocument()
    expect(batteryImg).toHaveAttribute('src', 'mock-battery-icon.svg')

    const powerIcon = container.querySelector('.mini-power-icon')
    const wifiIcon = container.querySelector('.mini-wifi-icon')
    const piIcon = container.querySelector('.mini-pi-icon')
    const commsIcon = container.querySelector('.mini-comms-icon')

    expect(powerIcon.style.backgroundColor).toBe('var(--success-green)')
    expect(wifiIcon.style.backgroundColor).toBe('var(--success-green)')
    expect(piIcon.style.backgroundColor).toBe('var(--success-green)')
    expect(commsIcon.style.backgroundColor).toBe('var(--success-green)')
  })

  it('renders red indicators when statuses are false', () => {
    useTurtlebotStatus.mockReturnValue({
      statusDTO: {
        isOn: false,
        batteryPercentage: 15,
        isWifiConnected: false,
        isRaspberryPiConnected: false,
        isCommsConnected: false,
      },
    })

    const { container } = render(<MinimizedStatusBar />)

    expect(getBatteryIcon).toHaveBeenCalledWith(15)
    expect(screen.getByAltText('Battery 15%')).toBeInTheDocument()

    const powerIcon = container.querySelector('.mini-power-icon')
    const wifiIcon = container.querySelector('.mini-wifi-icon')
    const piIcon = container.querySelector('.mini-pi-icon')
    const commsIcon = container.querySelector('.mini-comms-icon')

    expect(powerIcon.style.backgroundColor).toBe('var(--error-red)')
    expect(wifiIcon.style.backgroundColor).toBe('var(--error-red)')
    expect(piIcon.style.backgroundColor).toBe('var(--error-red)')
    expect(commsIcon.style.backgroundColor).toBe('var(--error-red)')
  })

  it('handles missing statusDTO safely', () => {
    useTurtlebotStatus.mockReturnValue({
      statusDTO: undefined,
    })

    const { container } = render(<MinimizedStatusBar />)

    expect(getBatteryIcon).toHaveBeenCalledWith(undefined)
    expect(screen.getByAltText('Battery undefined%')).toBeInTheDocument()

    const powerIcon = container.querySelector('.mini-power-icon')
    const wifiIcon = container.querySelector('.mini-wifi-icon')
    const piIcon = container.querySelector('.mini-pi-icon')
    const commsIcon = container.querySelector('.mini-comms-icon')

    expect(powerIcon.style.backgroundColor).toBe('var(--error-red)')
    expect(wifiIcon.style.backgroundColor).toBe('var(--error-red)')
    expect(piIcon.style.backgroundColor).toBe('var(--error-red)')
    expect(commsIcon.style.backgroundColor).toBe('var(--error-red)')
  })
})