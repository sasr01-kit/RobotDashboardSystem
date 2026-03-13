import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import PathExecutionBlock from '../../modules/turtlebot/components/PathExecutionBlock.jsx'
import { useModeContext } from '../../modules/turtlebot/modeUtil/ModeContext.js'
import { useWebSocketContext } from '../../modules/turtlebot/websocketUtil/WebsocketContext.js'

// Mocks animations to make testing more focused on functionality and more stable
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
    span: ({ children, ...props }) => <span {...props}>{children}</span>,
    button: ({ children, whileHover, whileTap, ...props }) => (
      <button {...props}>{children}</button>
    ),
  },
}))

// Mocking dependencies and contexts used in PathExecutionBlock to focus tests on its functionality without external factors
const sendMock = vi.fn()

vi.mock('../../modules/turtlebot/modeUtil/ModeContext.js', () => ({
  useModeContext: vi.fn(),
}))

vi.mock('../../modules/turtlebot/websocketUtil/WebsocketContext.js', () => ({
  useWebSocketContext: vi.fn(),
}))

// Tests for PathExecutionBlock to ensure it shows correct status and sends correct isPathModuleActive on button click
describe('PathExecutionBlock', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useWebSocketContext.mockReturnValue({ send: sendMock })
  })

  it('shows START when mode is not Running Path Module', () => {
    useModeContext.mockReturnValue({ mode: 'Teleoperating' })

    render(<PathExecutionBlock />)

    expect(screen.getByText('Status: Off')).toBeInTheDocument()
    expect(screen.getByRole('button')).toHaveTextContent('START')
  })

  it('sends isPathModuleActive true when starting', () => {
    useModeContext.mockReturnValue({ mode: 'Teleoperating' })

    render(<PathExecutionBlock />)

    fireEvent.click(screen.getByRole('button'))

    expect(sendMock).toHaveBeenCalledWith({ isPathModuleActive: true })
  })

  it('shows STOP when path module is running', () => {
    useModeContext.mockReturnValue({ mode: 'Running Path Module' })

    render(<PathExecutionBlock />)

    expect(screen.getByText('Status: On')).toBeInTheDocument()
    expect(screen.getByRole('button')).toHaveTextContent('STOP')
  })

  it('does not send again when already pending', async () => {
    vi.resetModules()
    const setPendingMock = vi.fn()

    vi.doMock('react', async () => {
      const actual = await vi.importActual('react')
      return {
        ...actual,
        useState: vi.fn((initial) => [true, setPendingMock]),
      }
    })

    vi.doMock('framer-motion', () => ({
      motion: {
        div: ({ children, ...props }) => <div {...props}>{children}</div>,
        span: ({ children, ...props }) => <span {...props}>{children}</span>,
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

    const { default: FreshPathExecutionBlock } = await import('../../modules/turtlebot/components/PathExecutionBlock.jsx')

    render(<FreshPathExecutionBlock />)

    const button = screen.getByRole('button')
    button.removeAttribute('disabled')
    button.disabled = false
    fireEvent.click(button)

    expect(sendMock).not.toHaveBeenCalled()
  })
})