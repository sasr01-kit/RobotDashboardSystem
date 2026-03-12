import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { PathLogDropdownNav } from '../../modules/turtlebot/components/PathLogDropdownNav.jsx'

// Mocks animations to make testing more focused on functionality and more stable
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, initial, animate, ...props }) => (
      <div {...props}>{children}</div>
    ),
  },
}))

const mockLogs = [
  {
    id: '1',
    goalType: 'global',
    timestamp: '2026-03-10T10:00:00Z',
  },
  {
    id: '2',
    goalType: 'intermediate',
    timestamp: '2026-03-11T15:30:00Z',
  },
]

// Tests for PathLogDropdownNav to ensure it renders the dropdown label, toggles the dropdown on label click, 
// calls onSelect with correct log id, and handles empty logs correctly
describe('PathLogDropdownNav', () => {
  it('renders the dropdown label', () => {
    render(<PathLogDropdownNav logs={mockLogs} onSelect={vi.fn()} />)

    expect(screen.getByText(/Path History/)).toBeInTheDocument()
  })

  it('is closed by default', () => {
    render(<PathLogDropdownNav logs={mockLogs} onSelect={vi.fn()} />)

    expect(screen.queryByRole('list')).not.toBeInTheDocument()
    expect(screen.queryByText(/global/i)).not.toBeInTheDocument()
  })

  it('opens the dropdown when the label is clicked', () => {
    render(<PathLogDropdownNav logs={mockLogs} onSelect={vi.fn()} />)

    fireEvent.click(screen.getByText(/Path History/))

    expect(screen.getByRole('list')).toBeInTheDocument()
    expect(screen.getByText(/global/i)).toBeInTheDocument()
    expect(screen.getByText(/intermediate/i)).toBeInTheDocument()
  })

  it('closes the dropdown when the label is clicked twice', () => {
    render(<PathLogDropdownNav logs={mockLogs} onSelect={vi.fn()} />)

    const label = screen.getByText(/Path History/)

    fireEvent.click(label)
    expect(screen.getByRole('list')).toBeInTheDocument()

    fireEvent.click(label)
    expect(screen.queryByRole('list')).not.toBeInTheDocument()
  })

  it('calls onSelect with the clicked log id', () => {
    const onSelect = vi.fn()

    render(<PathLogDropdownNav logs={mockLogs} onSelect={onSelect} />)

    fireEvent.click(screen.getByText(/Path History/))
    fireEvent.click(screen.getByText(/global/i))

    expect(onSelect).toHaveBeenCalledWith('1')
  })

  it('closes the dropdown after selecting a log', () => {
    const onSelect = vi.fn()

    render(<PathLogDropdownNav logs={mockLogs} onSelect={onSelect} />)

    fireEvent.click(screen.getByText(/Path History/))
    fireEvent.click(screen.getByText(/global/i))

    expect(onSelect).toHaveBeenCalledWith('1')
    expect(screen.queryByRole('list')).not.toBeInTheDocument()
  })

  it('renders no list items when logs is empty and opened', () => {
    render(<PathLogDropdownNav logs={[]} onSelect={vi.fn()} />)

    fireEvent.click(screen.getByText(/Path History/))

    expect(screen.getByRole('list')).toBeInTheDocument()
    expect(screen.queryByRole('listitem')).not.toBeInTheDocument()
  })
})