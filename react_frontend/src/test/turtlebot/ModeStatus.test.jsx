import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import ModeStatus from '../../modules/turtlebot/components/ModeStatus.jsx'
import { useModeContext } from '../../modules/turtlebot/modeUtil/ModeContext.js'

// Mocking the ModeContext to provide a specific mode value for testing
vi.mock('../../modules/turtlebot/modeUtil/ModeContext.js', () => ({
    useModeContext: vi.fn(),
}))


// Tests to ensure ModeStatus correctly renders the mode from context in uppercase
describe('ModeStatus', () => {
    it('renders teleoperating mode in uppercase', () => {
        useModeContext.mockReturnValue({ mode: 'Teleoperating' })

        render(<ModeStatus />)

        expect(screen.getByText('You are:')).toBeInTheDocument()
        expect(screen.getByText('TELEOPERATING')).toBeInTheDocument()
    })

    it('renders running path module mode in uppercase', () => {
    useModeContext.mockReturnValue({ mode: 'Running Path Module' })

    render(<ModeStatus />)

    expect(screen.getByText('You are:')).toBeInTheDocument()
    expect(screen.getByText('RUNNING PATH MODULE')).toBeInTheDocument()
  })

    it('renders unknown when mode is missing', () => {
        useModeContext.mockReturnValue({ mode: undefined })

        render(<ModeStatus />)

        expect(screen.getByText('UNKNOWN')).toBeInTheDocument()
    })
})