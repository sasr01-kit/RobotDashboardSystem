import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'

let subscriber 
let subscribeImpl

vi.mock('../../modules/turtlebot/websocketUtil/WebsocketContext', () => ({
  useWebSocketContext: () => ({
    subscribe: subscribeImpl,
  }),
}))

// Tests for useTurtlebotFeedback to ensure it updates correctly upon FEEDBACK_SUMMARY
// and FEEDBACK_ENTRY messages
describe('useTurtlebotFeedback', () => {
  beforeEach(() => {
    vi.resetModules()
    subscriber = undefined
    subscribeImpl = vi.fn((cb) => {
      subscriber = cb
      return () => {}
    })
    vi.spyOn(console, 'log').mockImplementation(() => {})
    vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  it('starts with default feedback state', async () => {
    const { useTurtlebotFeedback } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotFeedback.js'
    )

    const { result } = renderHook(() => useTurtlebotFeedback())

    expect(result.current.feedbackSummaryDTO).toBe(null)
    expect(result.current.feedbackEntries).toEqual([])
  })

  it('updates feedback summary from FEEDBACK_SUMMARY messages', async () => {
    const { useTurtlebotFeedback } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotFeedback.js'
    )

    const { result } = renderHook(() => useTurtlebotFeedback())

    act(() => {
      subscriber({
        type: 'FEEDBACK_SUMMARY',
        goodRatio: 0.75,
        badRatio: 0.25,
      })
    })

    expect(result.current.feedbackSummaryDTO).toEqual({
      goodRatio: 0.75,
      badRatio: 0.25,
    })
  })

  it('uses 0 defaults for missing summary ratios', async () => {
    const { useTurtlebotFeedback } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotFeedback.js'
    )

    const { result } = renderHook(() => useTurtlebotFeedback())

    act(() => {
      subscriber({
        type: 'FEEDBACK_SUMMARY',
        goodRatio: undefined,
        badRatio: undefined,
      })
    })

    expect(result.current.feedbackSummaryDTO).toEqual({
      goodRatio: 0,
      badRatio: 0,
    })
  })

  it('appends feedback entries from FEEDBACK_ENTRY messages', async () => {
    const { useTurtlebotFeedback } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotFeedback.js'
    )

    const { result } = renderHook(() => useTurtlebotFeedback())

    act(() => {
      subscriber({
        type: 'FEEDBACK_ENTRY',
        startPoint: 'A',
        endPoint: 'B',
        duration: 12,
        feedback: 'good',
      })
    })

    expect(result.current.feedbackEntries).toEqual([
      {
        startPoint: 'A',
        endPoint: 'B',
        duration: 12,
        feedback: 'good',
      },
    ])

    act(() => {
      subscriber({
        type: 'FEEDBACK_ENTRY',
        startPoint: 'B',
        endPoint: 'C',
        duration: 8,
        feedback: 'bad',
      })
    })

    expect(result.current.feedbackEntries).toEqual([
      {
        startPoint: 'A',
        endPoint: 'B',
        duration: 12,
        feedback: 'good',
      },
      {
        startPoint: 'B',
        endPoint: 'C',
        duration: 8,
        feedback: 'bad',
      },
    ])
  })

  it('does nothing when subscribe is missing', async () => {
    subscribeImpl = undefined

    const { useTurtlebotFeedback } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotFeedback.js'
    )

    const { result } = renderHook(() => useTurtlebotFeedback())

    expect(result.current.feedbackSummaryDTO).toBe(null)
    expect(result.current.feedbackEntries).toEqual([])
  })

  it('logs an error when parsing feedback throws', async () => {
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

    const { useTurtlebotFeedback } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotFeedback.js'
    )

    renderHook(() => useTurtlebotFeedback())

    const badPayload = {
      type: 'FEEDBACK_ENTRY',
      get startPoint() {
        throw new Error('bad payload')
      },
    }

    act(() => {
      subscriber(badPayload)
    })

    expect(errorSpy).toHaveBeenCalledWith('Failed to parse Turtlebot feedback')
  })
})