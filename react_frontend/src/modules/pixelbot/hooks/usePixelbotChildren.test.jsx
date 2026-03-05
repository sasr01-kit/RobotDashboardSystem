import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { usePixelbotChildren } from './usePixelbotChildren'
import { mockChildrenResponse } from '../__mocks__/data'

describe('usePixelbotChildren', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockChildrenResponse),
        })
      )
    )
  })

  it('fetches /pixelbot/children and maps to children with sessions (T24)', async () => {
    const { result } = renderHook(() => usePixelbotChildren())

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(fetch).toHaveBeenCalledWith('http://localhost:8080/pixelbot/children')
    expect(result.current.children).toHaveLength(1)
    expect(result.current.children[0].childId).toBe('c1')
    expect(result.current.children[0].name).toBe('Child One')
    expect(result.current.children[0].sessions).toHaveLength(2)
    expect(result.current.children[0].sessions[0].sessionId).toBe('s1')
  })
})
