import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'

let subscriber
let subscribeImpl

vi.mock('../../modules/turtlebot/websocketUtil/WebsocketContext', () => ({
  useWebSocketContext: () => ({
    subscribe: subscribeImpl,
  }),
}))

// Tests for useTurtlebotMap to ensure it initializes with default state and 
// updates correctly on MAP_UPDATE and POSE_UPDATE messages respectively
describe('useTurtlebotMap', () => {
  beforeEach(() => {
    vi.resetModules()
    subscriber = undefined
    subscribeImpl = vi.fn((cb) => {
      subscriber = cb
      return () => {}
    })
    vi.spyOn(console, 'log').mockImplementation(() => {})
  })

  it('starts with default map state', async () => {
    const { useTurtlebotMap } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotMap.js'
    )

    const { result } = renderHook(() => useTurtlebotMap())

    expect(result.current).toEqual({
      mapUrl: null,
      resolution: null,
      width: null,
      height: null,
      robotPose: null,
      humans: [],
      globalGoal: null,
      intermediateWaypoints: [],
    })
  })

  it('updates map data from MAP_DATA messages', async () => {
    const { useTurtlebotMap } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotMap.js'
    )

    const { result } = renderHook(() => useTurtlebotMap())

    act(() => {
      subscriber({
        type: 'MAP_DATA',
        mapData: {
          occupancyGridPNG: 'abc123',
          resolution: 0.05,
          width: 100,
          height: 200,
        },
      })
    })

    expect(result.current.mapUrl).toBe('data:image/png;base64,abc123')
    expect(result.current.resolution).toBe(0.05)
    expect(result.current.width).toBe(100)
    expect(result.current.height).toBe(200)
  })

  it('preserves previous map values when MAP_DATA fields are missing', async () => {
    const { useTurtlebotMap } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotMap.js'
    )

    const { result } = renderHook(() => useTurtlebotMap())

    act(() => {
      subscriber({
        type: 'MAP_DATA',
        mapData: {
          occupancyGridPNG: 'first-image',
          resolution: 0.05,
          width: 100,
          height: 200,
        },
      })
    })

    act(() => {
      subscriber({
        type: 'MAP_DATA',
        mapData: {
          occupancyGridPNG: null,
          resolution: undefined,
          width: undefined,
          height: undefined,
        },
      })
    })

    expect(result.current.mapUrl).toBe('data:image/png;base64,first-image')
    expect(result.current.resolution).toBe(0.05)
    expect(result.current.width).toBe(100)
    expect(result.current.height).toBe(200)
  })

  it('updates pose data from POSE_DATA messages', async () => {
    const { useTurtlebotMap } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotMap.js'
    )

    const { result } = renderHook(() => useTurtlebotMap())

    const robotPose = { x: 1, y: 2, theta: 3 }
    const humans = [{ id: 'h1', x: 4, y: 5 }]
    const globalGoal = { x: 8, y: 9 }
    const intermediateWaypoints = [{ x: 6, y: 7 }]

    act(() => {
      subscriber({
        type: 'POSE_DATA',
        robotPose,
        humans,
        globalGoal,
        intermediateWaypoints,
      })
    })

    expect(result.current.robotPose).toEqual(robotPose)
    expect(result.current.humans).toEqual(humans)
    expect(result.current.globalGoal).toEqual(globalGoal)
    expect(result.current.intermediateWaypoints).toEqual(intermediateWaypoints)
  })

  it('preserves previous pose values when POSE_DATA fields are missing', async () => {
    const { useTurtlebotMap } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotMap.js'
    )

    const { result } = renderHook(() => useTurtlebotMap())

    const robotPose = { x: 1, y: 2, theta: 3 }
    const humans = [{ id: 'h1' }]
    const globalGoal = { x: 9, y: 9 }
    const intermediateWaypoints = [{ x: 3, y: 4 }]

    act(() => {
      subscriber({
        type: 'POSE_DATA',
        robotPose,
        humans,
        globalGoal,
        intermediateWaypoints,
      })
    })

    act(() => {
      subscriber({
        type: 'POSE_DATA',
        robotPose: undefined,
        humans: undefined,
        globalGoal: undefined,
        intermediateWaypoints: undefined,
      })
    })

    expect(result.current.robotPose).toEqual(robotPose)
    expect(result.current.humans).toEqual(humans)
    expect(result.current.globalGoal).toEqual(globalGoal)
    expect(result.current.intermediateWaypoints).toEqual(intermediateWaypoints)
  })

  it('does nothing when subscribe is missing', async () => {
    subscribeImpl = undefined

    const { useTurtlebotMap } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotMap.js'
    )

    const { result } = renderHook(() => useTurtlebotMap())

    expect(result.current).toEqual({
      mapUrl: null,
      resolution: null,
      width: null,
      height: null,
      robotPose: null,
      humans: [],
      globalGoal: null,
      intermediateWaypoints: [],
    })
  })

  it('ignores websocket messages that are neither MAP_DATA nor POSE_DATA', async () => {
    const { useTurtlebotMap } = await import(
      '../../modules/turtlebot/hooks/useTurtlebotMap.js'
    )

    const { result } = renderHook(() => useTurtlebotMap())

    act(() => {
      subscriber({
        type: 'STATUS_UPDATE',
        robotPose: { x: 9, y: 9 },
      })
    })

    expect(result.current).toEqual({
      mapUrl: null,
      resolution: null,
      width: null,
      height: null,
      robotPose: null,
      humans: [],
      globalGoal: null,
      intermediateWaypoints: [],
    })
  })
})