import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { usePixelbotSession } from './usePixelbotSession'
import { mockSessionResponse } from '../__mocks__/data'

describe('usePixelbotSession', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockSessionResponse),
        })
      )
    )
  })

  it('fetches /pixelbot/children/:childId/sessions/:sessionId and returns session (T21, T22)', async () => {
    const { result } = renderHook(() => usePixelbotSession('c1', 's1'))

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8080/pixelbot/children/c1/sessions/s1'
    )
    expect(result.current.session).toBeDefined()
    expect(result.current.session.drawing).toHaveLength(1)
    expect(result.current.session.transcript).toHaveLength(1)
    expect(result.current.session.storySummary).toHaveLength(1)
    expect(result.current.session.speechWidth.intervention_count).toBe(5)
    expect(result.current.session.drawingWidth.surface_filled_percent).toBe(30)
  })

  it('does not fetch when childId is missing', async () => {
    const { result } = renderHook(() => usePixelbotSession(null, 's1'))
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })
    expect(fetch).not.toHaveBeenCalled()
    expect(result.current.session).toBeNull()
  })
})
