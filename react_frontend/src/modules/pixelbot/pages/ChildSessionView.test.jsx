import React from 'react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ChildSessionView from './ChildSessionView'
import { usePixelbotSession } from '../hooks/usePixelbotSession'
import { usePixelbotChildren } from '../hooks/usePixelbotChildren'
import { mockSessionResponse } from '../__mocks__/data'
import { mockChildrenResponse } from '../__mocks__/data'

vi.mock('../hooks/usePixelbotSession')
vi.mock('../hooks/usePixelbotChildren')

function renderWithRouter(childId = 'c1', sessionId = 's1') {
  return render(
    <MemoryRouter initialEntries={[`/pixelbot/session/${childId}/${sessionId}`]}>
      <Routes>
        <Route path="/pixelbot/session/:childId/:sessionId" element={<ChildSessionView />} />
      </Routes>
    </MemoryRouter>
  )
}

describe('ChildSessionView', () => {
  beforeEach(() => {
    const children = mockChildrenResponse.map((c) => ({
      childId: c.child_id,
      name: c.name,
      sessions: c.sessions.map((s) => ({ sessionId: s.sessionId })),
    }))
    usePixelbotChildren.mockReturnValue({ children, isLoading: false })
    usePixelbotSession.mockReturnValue({ session: mockSessionResponse, isLoading: false })
  })

  it('T21/T22: shows drawing, transcript, story summary and speech/drawing metrics', () => {
    renderWithRouter()
    expect(screen.getByText('Drawing')).toBeInTheDocument()
    expect(screen.getByText('Text Transcript')).toBeInTheDocument()
    expect(screen.getByText('Story Summary')).toBeInTheDocument()
    expect(screen.getByText('Speech Data')).toBeInTheDocument()
    expect(screen.getByText('Drawing Data')).toBeInTheDocument()
    expect(screen.getByText(/Child One/)).toBeInTheDocument()
    expect(screen.getByText(/Robot:/)).toBeInTheDocument()
    expect(screen.getByText('Number of intervention')).toBeInTheDocument()
    expect(screen.getByText('Amount of area filled')).toBeInTheDocument()
  })

  it('shows Loading when session is loading', () => {
    usePixelbotSession.mockReturnValue({ session: null, isLoading: true })
    renderWithRouter()
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })
})
