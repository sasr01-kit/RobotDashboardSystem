import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import TurtlebotFeedbackPage from '../../modules/turtlebot/pages/TurtlebotFeedbackPage.jsx'
import { useTurtlebotFeedback } from '../../modules/turtlebot/hooks/useTurtlebotFeedback.js'

vi.mock('../../modules/turtlebot/hooks/useTurtlebotFeedback.js', () => ({
  useTurtlebotFeedback: vi.fn(),
}))

vi.mock('../../modules/turtlebot/components/FeedbackSummaryChart.jsx', () => ({
  FeedbackSummaryChart: () => <div data-testid="feedback-summary-chart">FeedbackSummaryChart</div>,
}))

vi.mock('../../modules/turtlebot/components/FeedbackLogPanel.jsx', () => ({
  FeedbackLogPanel: ({ entries }) => (
    <div data-testid="feedback-log-panel">entries:{entries.length}</div>
  ),
}))

// Mocks animations to make testing more focused on functionality and more stable
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, initial, animate, ...props }) => <div {...props}>{children}</div>,
  },
}))

// Tests for TurtlebotFeedbackPage to ensure rendering reflects correct data from the hook 
// and safely render when there are no entries
describe('TurtlebotFeedbackPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders summary and feedback history sections', () => {
    useTurtlebotFeedback.mockReturnValue({
      feedbackEntries: [
        { id: '1', label: 'Good' },
        { id: '2', label: 'Bad' },
      ],
    })

    render(<TurtlebotFeedbackPage />)

    expect(screen.getByText('Feedback Summary')).toBeInTheDocument()
    expect(screen.getByText('Feedback History')).toBeInTheDocument()
    expect(screen.getByTestId('feedback-summary-chart')).toBeInTheDocument()
    expect(screen.getByTestId('feedback-log-panel')).toHaveTextContent('entries:2')
  })

  it('renders correctly with no feedback entries', () => {
    useTurtlebotFeedback.mockReturnValue({
      feedbackEntries: [],
    })

    render(<TurtlebotFeedbackPage />)

    expect(screen.getByText('Feedback Summary')).toBeInTheDocument()
    expect(screen.getByText('Feedback History')).toBeInTheDocument()
    expect(screen.getByTestId('feedback-log-panel')).toHaveTextContent('entries:0')
  })
})