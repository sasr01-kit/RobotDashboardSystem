import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'
import {
  useTurtlebotGoal,
  usePathHistoryActions,
  updateGlobalGoalState,
} from '../../modules/turtlebot/hooks/useTurtlebotGoal.js'

let subscriber // To hold the subscriber function passed to subscribe
let subscribeImpl
const sendMock = vi.fn()

vi.mock('../../modules/turtlebot/websocketUtil/WebsocketContext.js', () => ({
  useWebSocketContext: () => ({
    subscribe: subscribeImpl,
    send: sendMock,
  }),
}))

// Tests for useTurtlebotGoal to ensure it maps PATH_UPDATE messages into pathHistory correctly 
// and that path history actions send the correct websocket messages
describe('useTurtlebotGoal', () => {
  beforeEach(() => {
    subscriber = undefined
    subscribeImpl = (cb) => {
      subscriber = cb
      return () => {}
    }
    sendMock.mockClear()
    updateGlobalGoalState({
      pathHistory: [],
      isPathModuleActive: false,
      isDocked: false,
    })
  })

  it('maps PATH_UPDATE into frontend pathHistory', async () => {
    const { result } = renderHook(() => useTurtlebotGoal())

    act(() => {
      subscriber({
        type: 'PATH_UPDATE',
        isPathModuleActive: true,
        isDocked: false,
        pathHistory: [
          {
            id: '1',
            label: 'Goal A',
            timestamp: '2026-03-10T10:00:00Z',
            goalType: 'intermediate goal',
            fuzzyOutput: 'zone: medium; direction: front; output: straight',
            userFeedback: 'good',
          },
        ],
      })
    })

    await waitFor(() => {
      expect(result.current.pathHistory).toHaveLength(1)
      expect(result.current.pathHistory[0]).toEqual({
        id: '1',
        label: 'Goal A',
        timestamp: '2026-03-10T10:00:00Z',
        goalType: 'intermediate goal',
        fuzzy_output_goal: 'zone: medium; direction: front; output: straight',
        feedback: 'good',
      })
      expect(result.current.isPathModuleActive).toBe(true)
      expect(result.current.isDocked).toBe(false)
    })
  })

  it('path history actions send the correct websocket messages', () => {
    const { result } = renderHook(() => usePathHistoryActions())

    act(() => result.current.save())
    expect(sendMock).toHaveBeenCalledWith({ type: 'SAVE_PATH_HISTORY' })

    act(() => result.current.loadLatest())
    expect(sendMock).toHaveBeenCalledWith({ type: 'LOAD_LATEST_PATH_HISTORY' })

    act(() => result.current.clear())
    expect(sendMock).toHaveBeenCalledWith({ type: 'CLEAR_PATH_HISTORY' })
  })

  it('ignores non PATH_UPDATE websocket messages', async () => {
    const { result } = renderHook(() => useTurtlebotGoal())

    act(() => {
      subscriber({ type: 'STATUS_UPDATE', isPathModuleActive: true, isDocked: true })
    })

    await waitFor(() => {
      expect(result.current.pathHistory).toEqual([])
      expect(result.current.isPathModuleActive).toBe(false)
      expect(result.current.isDocked).toBe(false)
    })
  })

  it('maps missing userFeedback to empty string', async () => {
    const { result } = renderHook(() => useTurtlebotGoal())

    act(() => {
      subscriber({
        type: 'PATH_UPDATE',
        isPathModuleActive: true,
        isDocked: false,
        pathHistory: [
          {
            id: '2',
            label: 'Goal B',
            timestamp: '2026-03-11T10:00:00Z',
            goalType: 'global goal',
            fuzzyOutput: 'zone: low; direction: left; output: turn',
          },
        ],
      })
    })

    await waitFor(() => {
      expect(result.current.pathHistory[0].feedback).toBe('')
    })
  })

  it('falls back to previous flags and empty pathHistory when payload fields are missing', async () => {
    updateGlobalGoalState({
      pathHistory: [{ id: 'existing' }],
      isPathModuleActive: true,
      isDocked: true,
    })

    const { result } = renderHook(() => useTurtlebotGoal())

    act(() => {
      subscriber({
        type: 'PATH_UPDATE',
      })
    })

    await waitFor(() => {
      expect(result.current.pathHistory).toEqual([])
      expect(result.current.isPathModuleActive).toBe(true)
      expect(result.current.isDocked).toBe(true)
    })
  })

  it('returns current state when websocket subscribe is unavailable', () => {
    subscribeImpl = undefined
    updateGlobalGoalState({
      pathHistory: [{ id: 'seed' }],
      isPathModuleActive: true,
      isDocked: false,
    })

    const { result } = renderHook(() => useTurtlebotGoal())

    expect(result.current.pathHistory).toEqual([{ id: 'seed' }])
    expect(result.current.isPathModuleActive).toBe(true)
    expect(result.current.isDocked).toBe(false)
  })
})