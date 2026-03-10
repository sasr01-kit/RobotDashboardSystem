/** Shared mock API responses for Pixelbot unit tests (Pflichtenheft T20–T29). */

export const mockSummaryResponse = {
  totalSessionsThisMonth: 42,
  sessionsPerChild: 4,
  sessionsPerDay: 2,
  sessionsGrowthRate: 10,
  dailySessionCounts: { '1-3-2025': 2, '2-3-2025': 1 },
  colorScale: [],
}

export const mockChildrenResponse = [
  {
    child_id: 'c1',
    name: 'Child One',
    sessions: [{ sessionId: 's1' }, { sessionId: 's2' }],
  },
]

export const mockSessionResponse = {
  drawing: ['data:image/png;base64,abc'],
  transcript: [{ name: 'Robot', description: 'Hello' }],
  storySummary: [{ name: 'object', description: 'detected' }],
  speechWidth: {
    intervention_count: 5,
    total_word_count: 100,
    average_word_count_per_intervention: 20,
    std_word_count_per_intervention: 2,
  },
  drawingWidth: {
    surface_filled_percent: 30,
    stroke_count: 10,
    average_stroke_length: 5,
  },
}

export const mockRecapResponse = {
  name: 'Child One',
  engagement: {
    totalSessions: 2,
    sessionFrequencyTrend: [
      { month: 'Jan', count: 1 },
      { month: 'Feb', count: 2 },
    ],
  },
  expressiveness: {
    totalWordCount: 100,
    averageWordCount: 50,
    wordCountGrowthRate: [{ sessionId: 's1', wordCount: 40 }, { sessionId: 's2', wordCount: 60 }],
    speechTimeGrowthRate: [{ sessionId: 's1', speechTime: 120 }, { sessionId: 's2', speechTime: 180 }],
  },
  opennes: {
    averageIntimacyScore: 0.5,
    intimacyTrend: [{ sessionId: 's1', intimacy: 0.4 }, { sessionId: 's2', intimacy: 0.6 }],
  },
  drawing: {
    drawings: [],
    averageStrokeCount: 8,
    averageNumberColors: 3,
    averageFilledArea: 25,
  },
  story: {
    averageNumberObjects: 2,
    mostCommonObjects: ['ball'],
    objectDiversity: 0.5,
  },
}
