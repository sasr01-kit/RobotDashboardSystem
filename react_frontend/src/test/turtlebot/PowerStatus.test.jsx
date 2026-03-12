import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import PowerStatus from '../../modules/turtlebot/components/PowerStatus.jsx'

// Mocks animations to make testing more focused on functionality and more stable
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
  },
}))

// Tests by toggling isOn to ensure it correctly displays ON/OFF
describe('PowerStatus', () => {
  it('shows ON when isOn is true', () => {
    render(<PowerStatus isOn={true} />)
    expect(screen.getByText('ON')).toBeInTheDocument()
  })

  it('shows OFF when isOn is false', () => {
    render(<PowerStatus isOn={false} />)
    expect(screen.getByText('OFF')).toBeInTheDocument()
  })
})