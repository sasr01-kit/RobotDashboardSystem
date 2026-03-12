import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import DockingBlock from '../../modules/turtlebot/components/DockingBlock.jsx'
import { useTurtlebotStatus } from '../../modules/turtlebot/hooks/useTurtlebotStatus.js'
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

// Mocking dependencies and contexts used in DockingBlock to focus tests on its functionality without external factors
const sendMock = vi.fn()

vi.mock('../../modules/turtlebot/hooks/useTurtlebotStatus.js', () => ({
  useTurtlebotStatus: vi.fn(),
}))

vi.mock('../../modules/turtlebot/websocketUtil/WebsocketContext.js', () => ({
  useWebSocketContext: vi.fn(),
}))

// Tests for DockingBlock to ensure it shows correct status and sends correct dockStatus on button click
describe('DockingBlock', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useWebSocketContext.mockReturnValue({ send: sendMock })
  })

  it('shows UNDOCK when robot is docked', () => {
    useTurtlebotStatus.mockReturnValue({
      statusDTO: { isDocked: true },
    })

    render(<DockingBlock />)

    expect(screen.getByText('Status : Docked')).toBeInTheDocument()
    expect(screen.getByRole('button')).toHaveTextContent('UNDOCK')
  })

  it('sends dockStatus true when currently undocked', () => {
    useTurtlebotStatus.mockReturnValue({
      statusDTO: { isDocked: false },
    })

    render(<DockingBlock />)

    fireEvent.click(screen.getByRole('button'))

    expect(sendMock).toHaveBeenCalledWith({ dockStatus: true })
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

    vi.doMock('../../modules/turtlebot/hooks/useTurtlebotStatus.js', () => ({
      useTurtlebotStatus: () => ({ statusDTO: { isDocked: false } }),
    }))

    vi.doMock('../../modules/turtlebot/websocketUtil/WebsocketContext.js', () => ({
      useWebSocketContext: () => ({ send: sendMock }),
    }))

    const { default: FreshDockingBlock } = await import('../../modules/turtlebot/components/DockingBlock.jsx')

    render(<FreshDockingBlock />)

    const button = screen.getByRole('button')
    button.removeAttribute('disabled')
    button.disabled = false
    fireEvent.click(button)

    expect(sendMock).not.toHaveBeenCalled()
  })
})