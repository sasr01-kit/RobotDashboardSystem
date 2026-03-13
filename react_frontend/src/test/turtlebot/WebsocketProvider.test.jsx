import React from 'react'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, act, waitFor } from '@testing-library/react'
import WebSocketProvider from '../../modules/turtlebot/websocketUtil/WebsocketProvider.jsx'
import { useWebSocketContext } from '../../modules/turtlebot/websocketUtil/WebsocketContext.js'

class MockWebSocket {
  static OPEN = 1
  static instances = []

  constructor(url) {
    this.url = url
    this.readyState = 0
    this.send = vi.fn()
    this.close = vi.fn(() => {
      if (this.onclose) this.onclose()
    })

    this.onopen = null
    this.onclose = null
    this.onerror = null
    this.onmessage = null

    MockWebSocket.instances.push(this)
  }
}

// Mock consumer component for testing the provider
function TestConsumer() {
  const { send, subscribe, isConnected } = useWebSocketContext()

  React.useEffect(() => {
    const unsubscribe = subscribe((data) => {
      window.__lastMessage = data
    })
    return unsubscribe
  }, [subscribe])

  return (
    <div>
      <div data-testid="connected">{String(isConnected)}</div>
      <button onClick={() => send({ hello: 'world' })}>Send</button>
    </div>
  )
}

function UnsubscribingConsumer() {
  const { subscribe } = useWebSocketContext()

  React.useEffect(() => {
    const callback = (data) => {
      window.__unsubTestMessage = data
    }

    const unsubscribe = subscribe(callback)
    unsubscribe()
  }, [subscribe])

  return <div>Unsubscribed</div>
}

// Tests for WebSocketProvider to ensure proper websocket connection management and 
// it can reconnect properly if an error occurs
describe('WebSocketProvider', () => {
  let originalWebSocket
  let logSpy
  let warnSpy
  let errorSpy

  beforeEach(() => {
    vi.useFakeTimers()

    MockWebSocket.instances = []
    window.__lastMessage = undefined
    window.__unsubTestMessage = undefined

    originalWebSocket = global.WebSocket
    global.WebSocket = MockWebSocket

    logSpy = vi.spyOn(console, 'log').mockImplementation(() => {})
    warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {})
    errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  afterEach(() => {
    vi.useRealTimers()
    global.WebSocket = originalWebSocket
    vi.restoreAllMocks()
  })

  it('creates a websocket connection on mount', () => {
    render(
      <WebSocketProvider>
        <TestConsumer />
      </WebSocketProvider>
    )

    expect(MockWebSocket.instances).toHaveLength(1)
    expect(MockWebSocket.instances[0].url).toBe('ws://localhost:8080/ws')
    expect(logSpy).toHaveBeenCalledWith('[WS] Attempting connection...')
  })

  it('sets isConnected to true when the socket opens', () => {
    render(
        <WebSocketProvider>
        <TestConsumer />
        </WebSocketProvider>
    )

    const ws = MockWebSocket.instances[0]

    act(() => {
        ws.readyState = MockWebSocket.OPEN
        ws.onopen()
    })

    expect(screen.getByTestId('connected')).toHaveTextContent('true')
    })

  it('sets isConnected to false and reconnects after close', () => {
    vi.useFakeTimers()

    render(
        <WebSocketProvider>
        <TestConsumer />
        </WebSocketProvider>
    )

    const firstWs = MockWebSocket.instances[0]

    act(() => {
        firstWs.readyState = MockWebSocket.OPEN
        firstWs.onopen()
    })

    expect(screen.getByTestId('connected')).toHaveTextContent('true')

    act(() => {
        firstWs.onclose()
    })

    expect(screen.getByTestId('connected')).toHaveTextContent('false')

    act(() => {
        vi.advanceTimersByTime(1000)
    })

    expect(MockWebSocket.instances).toHaveLength(2)

    vi.useRealTimers()
    })

  it('closes the socket when an error occurs', () => {
    render(
      <WebSocketProvider>
        <TestConsumer />
      </WebSocketProvider>
    )

    const ws = MockWebSocket.instances[0]
    const err = new Error('socket failed')

    act(() => {
      ws.onerror(err)
    })

    expect(errorSpy).toHaveBeenCalledWith('[WS] Error:', err)
    expect(ws.close).toHaveBeenCalled()
  })

  it('sends json when the socket is open', () => {
    render(
      <WebSocketProvider>
        <TestConsumer />
      </WebSocketProvider>
    )

    const ws = MockWebSocket.instances[0]
    ws.readyState = MockWebSocket.OPEN

    act(() => {
      screen.getByText('Send').click()
    })

    expect(ws.send).toHaveBeenCalledWith(JSON.stringify({ hello: 'world' }))
  })

  it('warns when trying to send while socket is not open', () => {
    render(
      <WebSocketProvider>
        <TestConsumer />
      </WebSocketProvider>
    )

    const ws = MockWebSocket.instances[0]
    ws.readyState = 0

    act(() => {
      screen.getByText('Send').click()
    })

    expect(ws.send).not.toHaveBeenCalled()
    expect(warnSpy).toHaveBeenCalledWith('[WS] Tried to send but socket not open')
  })

 it('notifies subscribers with parsed websocket messages', () => {
    render(
        <WebSocketProvider>
        <TestConsumer />
        </WebSocketProvider>
    )

    const ws = MockWebSocket.instances[0]

    act(() => {
        ws.onmessage({
        data: JSON.stringify({ type: 'STATUS_UPDATE', isOn: true }),
        })
    })

    expect(window.__lastMessage).toEqual({
        type: 'STATUS_UPDATE',
        isOn: true,
    })
    })

  it('does not notify a subscriber after it unsubscribes', () => {
    render(
      <WebSocketProvider>
        <UnsubscribingConsumer />
      </WebSocketProvider>
    )

    const ws = MockWebSocket.instances[0]

    act(() => {
      ws.onmessage({
        data: JSON.stringify({ type: 'STATUS_UPDATE', isOn: true }),
      })
    })

    expect(window.__unsubTestMessage).toBeUndefined()
  })

  it('logs a parse error for invalid message data', () => {
    render(
      <WebSocketProvider>
        <TestConsumer />
      </WebSocketProvider>
    )

    const ws = MockWebSocket.instances[0]

    act(() => {
      ws.onmessage({
        data: 'not-valid-json',
      })
    })

    expect(errorSpy).toHaveBeenCalledWith(
      '[WS] Parse error:',
      expect.any(Error)
    )
  })

  it('closes the current socket on unmount', () => {
    const { unmount } = render(
      <WebSocketProvider>
        <TestConsumer />
      </WebSocketProvider>
    )

    const ws = MockWebSocket.instances[0]

    unmount()

    expect(ws.close).toHaveBeenCalled()
  })
})