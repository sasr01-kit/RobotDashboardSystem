import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { ModeProvider } from '../../modules/turtlebot/modeUtil/ModeProvider.jsx'
import { useModeContext } from '../../modules/turtlebot/modeUtil/ModeContext.js'
import { useTurtlebotStatus } from '../../modules/turtlebot/hooks/useTurtlebotStatus.js'

vi.mock('../../modules/turtlebot/hooks/useTurtlebotStatus.js', () => ({
  useTurtlebotStatus: vi.fn(),
}))

// Mock component to consume the ModeContext for testing purposes
function TestConsumer() {
  const { mode, setMode } = useModeContext()

  return (
    <div>
      <div data-testid="mode">{mode}</div>
      <button onClick={() => setMode('Idle')}>Set Idle</button>
    </div>
  )
}

// Tests for ModeProvider to ensure it provides the correct mode value and updates based on 
// statusDTO.mode, as well as allowing consumers to update mode with setMode, and throwing an error when used outside of a provider
describe('ModeProvider', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('starts with Teleoperating by default', () => {
    useTurtlebotStatus.mockReturnValue({
      statusDTO: undefined,
    })

    render(
      <ModeProvider>
        <TestConsumer />
      </ModeProvider>
    )

    expect(screen.getByTestId('mode')).toHaveTextContent('Teleoperating')
  })

  it('updates mode from statusDTO.mode', () => {
    useTurtlebotStatus.mockReturnValue({
      statusDTO: {
        mode: 'Running Path Module',
      },
    })

    render(
      <ModeProvider>
        <TestConsumer />
      </ModeProvider>
    )

    expect(screen.getByTestId('mode')).toHaveTextContent('Running Path Module')
  })

  it('keeps default mode when statusDTO.mode is missing', () => {
    useTurtlebotStatus.mockReturnValue({
      statusDTO: {},
    })

    render(
      <ModeProvider>
        <TestConsumer />
      </ModeProvider>
    )

    expect(screen.getByTestId('mode')).toHaveTextContent('Teleoperating')
  })

  it('allows consumers to update mode with setMode', () => {
    useTurtlebotStatus.mockReturnValue({
      statusDTO: undefined,
    })

    render(
      <ModeProvider>
        <TestConsumer />
      </ModeProvider>
    )

    fireEvent.click(screen.getByText('Set Idle'))

    expect(screen.getByTestId('mode')).toHaveTextContent('Idle')
  })
})