import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { usePixelbotChildren } from '../../modules/pixelbot/hooks/usePixelbotChildren'
import { mockChildrenResponse } from '../../modules/pixelbot/__mocks__/data'

// Tests for usePixelbotChildren to ensure it fetches children data correctly, handles loading and error states, 
// and maps the response to the expected format
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

  it('sets error when fetch fails', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() => Promise.reject(new Error('Network error')))
    )
    vi.spyOn(console, 'error').mockImplementation(() => {})

    const { result } = renderHook(() => usePixelbotChildren())

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.error).toBe('Failed to fetch children data.')
    expect(result.current.children).toBeNull()
  })

  it('sets error when response is not ok', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: false,
          json: () => Promise.resolve([]),
        })
      )
    )
    vi.spyOn(console, 'error').mockImplementation(() => {})

    const { result } = renderHook(() => usePixelbotChildren())

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.error).toBe('Failed to fetch children data.')
    expect(result.current.children).toBeNull()
  })
})
