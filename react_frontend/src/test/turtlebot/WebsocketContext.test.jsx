import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import WebSocketContext, {
  useWebSocketContext,
} from '../../modules/turtlebot/websocketUtil/WebsocketContext.js'

// Mock consumer component for testing the context 
function TestConsumer() {
  const value = useWebSocketContext()

  return (
    <div>
      {value === null ? 'null-context' : `connected:${String(value.isConnected)}`}
    </div>
  )
}

// Tests for WebSocketContext to ensures it throws an error when used without its provider
// and returns websocket functionalities to its consumers 
describe('WebSocketContext', () => {
  it('returns null when used without a provider', () => {
    render(<TestConsumer />)

    expect(screen.getByText('null-context')).toBeInTheDocument()
  })

  it('returns the provided context value', () => {
    render(
      <WebSocketContext.Provider
        value={{
          send: () => {},
          subscribe: () => () => {},
          isConnected: true,
        }}
      >
        <TestConsumer />
      </WebSocketContext.Provider>
    )

    expect(screen.getByText('connected:true')).toBeInTheDocument()
  })
})