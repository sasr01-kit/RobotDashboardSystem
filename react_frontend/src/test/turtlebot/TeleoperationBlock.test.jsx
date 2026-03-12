import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import TeleoperationBlock from '../../modules/turtlebot/components/TeleoperationBlock.jsx'
import { useModeContext } from '../../modules/turtlebot/modeUtil/ModeContext.js'
import { useWebSocketContext } from '../../modules/turtlebot/websocketUtil/WebsocketContext.js'

// Mocks animations to make testing more focused on functionality and more stable
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
    button: ({ children, whileHover, whileTap, ...props }) => (
      <button {...props}>{children}</button>
    ),
  },
}))

// Mocking dependencies and contexts used in TeleoperationBlock to focus tests on its functionality without external factors
const sendMock = vi.fn()

vi.mock('../../modules/turtlebot/modeUtil/ModeContext.js', () => ({
  useModeContext: vi.fn(),
}))

vi.mock('../../modules/turtlebot/websocketUtil/WebsocketContext.js', () => ({
  useWebSocketContext: vi.fn(),
}))

vi.mock('../../modules/turtlebot/components/TeleoperationButton.jsx', () => ({
  default: ({ direction, onClick }) => (
    <button onClick={() => onClick(direction)}>{direction}</button>
  ),
}))

// Tests for TeleoperationBlock to ensure it sends correct commands on button clicks and renders disabled state when not in teleoperating mode
describe('TeleoperationBlock', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useModeContext.mockReturnValue({ mode: 'Teleoperating' })
    useWebSocketContext.mockReturnValue({ send: sendMock })
  })

  it('sends FORWARD when UP is clicked', () => {
    render(<TeleoperationBlock />)

    fireEvent.click(screen.getByText('UP'))

    expect(sendMock).toHaveBeenCalledWith({ command: 'FORWARD' })
    expect(screen.getByText('Sent: FORWARD')).toBeInTheDocument()
  })

  it('sends BACKWARD when DOWN is clicked', () => {
    render(<TeleoperationBlock />)

    fireEvent.click(screen.getByText('DOWN'))

    expect(sendMock).toHaveBeenCalledWith({ command: 'BACKWARD' })
    expect(screen.getByText('Sent: BACKWARD')).toBeInTheDocument()
  })

  it('sends LEFT when LEFT is clicked', () => {
    render(<TeleoperationBlock />)

    fireEvent.click(screen.getByText('LEFT'))

    expect(sendMock).toHaveBeenCalledWith({ command: 'LEFT' })
    expect(screen.getByText('Sent: LEFT')).toBeInTheDocument()
  })

  it('sends RIGHT when RIGHT is clicked', () => {
    render(<TeleoperationBlock />)

    fireEvent.click(screen.getByText('RIGHT'))

    expect(sendMock).toHaveBeenCalledWith({ command: 'RIGHT' })
    expect(screen.getByText('Sent: RIGHT')).toBeInTheDocument()
  })

  it('sends ROTATE_LEFT when ROTATE_CCW is clicked', () => {
    render(<TeleoperationBlock />)

    fireEvent.click(screen.getByText('ROTATE_CCW'))

    expect(sendMock).toHaveBeenCalledWith({ command: 'ROTATE_LEFT' })
    expect(screen.getByText('Sent: ROTATE_LEFT')).toBeInTheDocument()
  })

  it('sends ROTATE_RIGHT when ROTATE_CW is clicked', () => {
    render(<TeleoperationBlock />)

    fireEvent.click(screen.getByText('ROTATE_CW'))

    expect(sendMock).toHaveBeenCalledWith({ command: 'ROTATE_RIGHT' })
    expect(screen.getByText('Sent: ROTATE_RIGHT')).toBeInTheDocument()
  })

  it('sends STOP when STOP is clicked', () => {
    render(<TeleoperationBlock />)

    fireEvent.click(screen.getByText('STOP'))

    expect(sendMock).toHaveBeenCalledWith({ command: 'STOP' })
    expect(screen.getByText('Sent: STOP')).toBeInTheDocument()
  })

  it('renders disabled class when not teleoperating', () => {
    useModeContext.mockReturnValue({ mode: 'Idle' })

    const { container } = render(<TeleoperationBlock />)

    expect(container.querySelector('.teleoperation-block')?.className).toContain('disabled')
  })

  it('ignores unknown commands', async () => {
    vi.resetModules()

    vi.doMock('framer-motion', () => ({
      motion: {
        div: ({ children, ...props }) => <div {...props}>{children}</div>,
        button: ({ children, whileHover, whileTap, ...props }) => (
          <button {...props}>{children}</button>
        ),
      },
    }))

    vi.doMock('../../modules/turtlebot/modeUtil/ModeContext.js', () => ({
      useModeContext: () => ({ mode: 'Teleoperating' }),
    }))

    vi.doMock('../../modules/turtlebot/websocketUtil/WebsocketContext.js', () => ({
      useWebSocketContext: () => ({ send: sendMock }),
    }))

    vi.doMock('../../modules/turtlebot/components/TeleoperationButton.jsx', () => ({
      default: ({ onClick }) => (
        <button onClick={() => onClick('UNKNOWN')}>UNKNOWN</button>
      ),
    }))

    const { default: FreshTeleoperationBlock } = await import('../../modules/turtlebot/components/TeleoperationBlock.jsx')

    render(<FreshTeleoperationBlock />)

    fireEvent.click(screen.getAllByText('UNKNOWN')[0])

    expect(sendMock).not.toHaveBeenCalled()
    expect(screen.queryByText(/Sent:/)).not.toBeInTheDocument()
  })
})