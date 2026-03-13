import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent, act } from '@testing-library/react'
import TeleoperationButton from '../../modules/turtlebot/components/TeleoperationButton.jsx'

// Mocks animations to make testing more focused on functionality and more stable
vi.mock('framer-motion', () => ({
  motion: {
    button: ({ children, whileHover, whileTap, ...props }) => (
      <button {...props}>{children}</button>
    ),
  },
}))

// Tests for TeleoperationButton to ensure it calls onClick with correct direction 
// and adds clicked class briefly for checking
describe('TeleoperationButton', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('calls onClick with direction', () => {
    const onClick = vi.fn()

    render(
      <TeleoperationButton
        direction="UP"
        icon={<span>icon</span>}
        onClick={onClick}
      />
    )

    fireEvent.click(screen.getByRole('button'))
    expect(onClick).toHaveBeenCalledWith('UP')
  })

    it('adds clicked class briefly after click', () => {
    const onClick = vi.fn()

    render(
        <TeleoperationButton
        direction="UP"
        icon={<span>icon</span>}
        onClick={onClick}
        />
    )

    const button = screen.getByRole('button')

    fireEvent.click(button)

    expect(button.className).toContain('clicked')

    act(() => {
        vi.advanceTimersByTime(150)
    })

    expect(button.className).not.toContain('clicked')
    })
})