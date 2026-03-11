import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'
import {
  useTurtlebotStatus,
  updateGlobalStatusState,
} from '../../modules/turtlebot/hooks/useTurtlebotStatus.js'

let subscriber // To hold the subscriber function passed to subscribe
let subscribeImpl

vi.mock('../../modules/turtlebot/websocketUtil/WebsocketContext.js', () => ({
  useWebSocketContext: () => ({
    subscribe: subscribeImpl,
  }),
}))

// Tests for useTurtlebotStatus to ensure it initializes with default state and updates correctly on STATUS_UPDATE messages
describe('useTurtlebotStatus', () => {
  beforeEach(() => {
    subscriber = undefined
    subscribeImpl = (cb) => {
      subscriber = cb
      return () => {}
    }
    updateGlobalStatusState({
      isOn: false,
      batteryPercentage: null,
      isWifiConnected: false,
      isCommsConnected: false,
      isRaspberryPiConnected: false,
      mode: 'Teleoperating',
      isDocked: true,
    })
  })

  it('starts with default state', () => {
    const { result } = renderHook(() => useTurtlebotStatus())

    expect(result.current.statusDTO.isOn).toBe(false)
    expect(result.current.statusDTO.mode).toBe('Teleoperating')
    expect(result.current.error).toBe(null)
  })

  it('updates state from STATUS_UPDATE messages', async () => {
    const { result } = renderHook(() => useTurtlebotStatus())

    act(() => {
      subscriber({
        type: 'STATUS_UPDATE',
        isOn: true,
        batteryPercentage: 88,
        isWifiConnected: true,
        isCommsConnected: true,
        isRaspberryPiConnected: true,
        mode: 'Running Path Module',
        isDocked: false,
      })
    })

    await waitFor(() => {
      expect(result.current.statusDTO.isOn).toBe(true)
      expect(result.current.statusDTO.batteryPercentage).toBe(88)
      expect(result.current.statusDTO.mode).toBe('Running Path Module')
      expect(result.current.statusDTO.isDocked).toBe(false)
    })
  })

  it('sets an error when parsing the status payload throws', async () => {
    const { result } = renderHook(() => useTurtlebotStatus())

    const badMessage = {}
    Object.defineProperty(badMessage, 'type', {
      get() {
        throw new Error('bad status payload')
      },
    })

    act(() => {
      subscriber(badMessage)
    })

    await waitFor(() => {
      expect(result.current.error).toBe('Failed to parse Turtlebot status')
    })
  })

  it('ignores websocket messages that are not STATUS_UPDATE', async () => {
    const { result } = renderHook(() => useTurtlebotStatus())

    act(() => {
      subscriber({
        type: 'POSE_DATA',
        isOn: true,
        mode: 'Running Path Module',
      })
    })

    await waitFor(() => {
      expect(result.current.statusDTO.isOn).toBe(false)
      expect(result.current.statusDTO.mode).toBe('Teleoperating')
      expect(result.current.error).toBe(null)
    })
  })

  it('returns current state when subscribe is unavailable', () => {
    subscribeImpl = undefined

    const { result } = renderHook(() => useTurtlebotStatus())

    expect(result.current.statusDTO.isOn).toBe(false)
    expect(result.current.statusDTO.mode).toBe('Teleoperating')
    expect(result.current.error).toBe(null)
  })
})