import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import ModeContext, { useModeContext } from '../../modules/turtlebot/modeUtil/ModeContext.js'

// Mock component to consume the ModeContext for testing purposes
function TestConsumer() {
  const { mode } = useModeContext()
  return <div>{mode}</div>
}

// Tests for ModeContext to ensure it provides the correct mode value and throws an error when used outside of a provider
describe('ModeContext', () => {
  it('returns the provided context value', () => {
    render(
      <ModeContext.Provider value={{ mode: 'Running Path Module', setMode: () => {} }}>
        <TestConsumer />
      </ModeContext.Provider>
    )

    expect(screen.getByText('Running Path Module')).toBeInTheDocument()
  })

  it('throws when used outside a ModeProvider', () => {
    expect(() => render(<TestConsumer />)).toThrow(
      'useModeContext must be used within a ModeProvider'
    )
  })
})