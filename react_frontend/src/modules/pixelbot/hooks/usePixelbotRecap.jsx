import { useEffect, useState } from "react";

export function usePixelbotRecap(childId) {
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

    const fetchData = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const res = await fetch(`http://localhost:8080/pixelbot/children/${childId}/recap`);
        if (!res.ok) throw new Error("Child recap not found");

        const data = await res.json();

        // Calculate trend percentage from sessionFrequencyTrend (last 2 months)
        const sessionTrend = data.engagement?.sessionFrequencyTrend || [];
        let sessionTrendPercentage = 0;
        if (sessionTrend.length >= 2) {
          const lastMonth = sessionTrend[sessionTrend.length - 1].count;
          const previousMonth = sessionTrend[sessionTrend.length - 2].count;
          if (previousMonth > 0) {
            sessionTrendPercentage = ((lastMonth - previousMonth) / previousMonth) * 100;
          }
        }

        const recapDTO = {
          name : data.name,
          // Session frequency data for line chart
          sessionFrequencyData: (data.engagement?.sessionFrequencyTrend || []).map(item => ({
            label: item.month,
            value: item.count
          })),
          
          // Word count data for bar chart
          wordCountData: (data.expressiveness?.wordCountGrowthRate || []).map(item => ({
            label: item.sessionId,
            value: item.wordCount
          })),
          
          // Speech time data for line chart
          speechTimeData: (data.expressiveness?.speechTimeGrowthRate || []).map(item => ({
            label: item.sessionId,
            value: item.speechTime / 60 // Convert to minutes
          })),
          
          // Intimacy score data for line chart
          intimacyScoreData: (data.opennes?.intimacyTrend || []).map(item => ({
            label: item.sessionId,
            value: item.intimacy
          })),
          
          // Drawings 
          drawings: (data.drawing?.drawings || []).map(d => `data:image/png;base64,${d.base64}`),
          
          // Metric values
          metricValues: {
            totalSessions: data.engagement?.totalSessions || 0,
            sessionTrendPercentage: sessionTrendPercentage.toFixed(1),
            
            totalWordCount: data.expressiveness?.totalWordCount || 0,
            averageWordCount: data.expressiveness?.averageWordCount || 0,
            
            averageIntimacyScore: data.opennes?.averageIntimacyScore || 0,
            
            averageStrokeCount: data.drawing?.averageStrokeCount || 0,
            averageNumberColors: data.drawing?.averageNumberColors || 0,
            averageFilledArea: data.drawing?.averageFilledArea || 0,
            
            averageNumberObjects: data.story?.averageNumberObjects || 0,
            mostCommonObjects: data.story?.mostCommonObjects || [],
            objectDiversity: data.story?.objectDiversity || 0
          }
        };

        setChild(recapDTO);
        setSession(null);
      } catch (err) {
        setError("Failed to load data.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [childId]);

  return { child, session, isLoading, error };
}
