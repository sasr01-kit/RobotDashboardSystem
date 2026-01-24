import { useEffect, useState } from "react";

// MOCK DATA FOR SESSION
const MOCK_STORY_SUMMARY = [
    { name: 'Sun', description: 'A yellow sun with rays, drawn in the top left corner.' },
    { name: 'Cloud', description: 'Three blue clouds drawn across the top of the page.' },
    { name: 'Grass', description: 'Green grass drawn along the bottom of the page, covering the whole width.' },
    { name: 'House', description: 'A simple house with a triangular roof, placed towards the top center.' },
    { name: 'Tree', description: 'A tall tree next to the house with green leaves.' },
];

const MOCK_TRANSCRIPT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quam velit, vulputate eu pharetra nec, mattis ac neque. Duis vulputate commodo lectus, blandit id. Sed rhoncus, tortor sed eleifend tristique, tortor mauris molestie elit, et lacinia ipsum quam nec dui. Quisque nec mauris elit. Duis vulputate commodo lectus, blandit id. Sed rhoncus, tortor sed eleifend tristique, tortor mauris molestie elit, et lacinia ipsum quam nec dui.";

const MOCK_SPEECH_DATA = {
    globalAvgWordCount: 180,
    globalAvgSpeechTime: 16,
    globalAvgIntimacyScore: 7,
    globalAvgScoreLength: 14
};

const MOCK_DRAWING_STATS = {
    surfacePercentage: 65,
    numStrokes: 120,
    avgStrokeLength: 15,
    stdStrokeLength: 5,
    numberColorsUsed: 8,
    numberPenSizedUsed: 3
};

const MOCK_DRAWING_DATA = [
    { imagePath: 'https://placehold.co/250x200' },
];

// MOCK DATA FOR CHILD RECAP
const MOCK_PLACEHOLDER_IMAGES = [
    'https://placehold.co/250x200',
    'https://placehold.co/250x200',
    'https://placehold.co/250x200'
];

const MOCK_WORD_COUNT_DATA = Array.from({ length: 10 }, (_, i) => ({
    label: `Session ${i + 1}`,
    value: Math.floor(Math.random() * 200) + 150
}));

// Speech time per session (in minutes)
const MOCK_SPEECH_TIME_DATA = Array.from({ length: 10 }, (_, i) => ({
    label: `Session ${i + 1}`,
    value: Math.floor(Math.random() * 15) + 10 // Random value between 10-25 minutes
}));

const MOCK_COLORS_USED_DATA = new Map([
    ['Green', [45, 52, 38].map((v, i) => ({ label: `Session ${i + 1}`, value: v }))],
    ['Light Green', [32, 41, 35].map((v, i) => ({ label: `Session ${i + 1}`, value: v }))],
    ['Teal', [28, 35, 42].map((v, i) => ({ label: `Session ${i + 1}`, value: v }))]
]);

const MOCK_METRIC_VALUES = {
    totalSessions: 16,
    totalSessionsTrend: "-5",
    totalWordCount: 13450,
    totalWordCountTrend: "+8500",
    averageIntimacyScore: 70,
    averageIntimacyScoreTrend: "+10"
};

// ============================================
// HOOK
// ============================================

export function usePixelbotSession(childId, sessionId = null) {
    const [session, setSession] = useState(null);
    const [child, setChild] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Early return if no childId
        if (!childId) {
            setChild(null);
            setSession(null);
            return;
        }

        // Fetch function defined inside useEffect for clean dependency management
        const fetchData = async () => {
            setIsLoading(true);
            setError(null);

            try {
                if (!sessionId) {
                    // Fetch child recap data
                    // TODO: Implement actual API call
                    // const response = await fetch(`/api/children/${childId}/recap`);
                    // const data = await response.json();
                    // setChild(data);

                    // Mock data for now
                    setChild({
                        childName: "Child name",
                        drawings: MOCK_PLACEHOLDER_IMAGES,
                        wordCountData: MOCK_WORD_COUNT_DATA,
                        speechTimeData: MOCK_SPEECH_TIME_DATA,
                        colorsUsedData: MOCK_COLORS_USED_DATA,
                        metricValues: MOCK_METRIC_VALUES
                    });
                    setSession(null); // Clear session when viewing recap
                } else {
                    // Fetch specific session data
                    // TODO: Implement actual API call
                    // const response = await fetch(`/api/children/${childId}/sessions/${sessionId}`);
                    // const data = await response.json();
                    // setSession(data);

                    // Mock data for now
                    setSession({
                        sessionId: sessionId,
                        storySummary: MOCK_STORY_SUMMARY,
                        transcript: MOCK_TRANSCRIPT,
                        drawing: MOCK_DRAWING_DATA,
                        benchmarks: MOCK_SPEECH_DATA,
                        drawingWidth: MOCK_DRAWING_STATS
                    });
                    setChild(null); // Clear child when viewing session
                }
            } catch (err) {
                setError("Failed to load data.");
                console.error("usePixelbotSession fetch error:", err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [childId, sessionId]); // Re-fetch when childId or sessionId changes

    return { child, session, isLoading, error };
}