import { useEffect, useState } from "react";
/*  TEMPORARY MOCK DELETE LATER!!!!!*/
export function useTurtlebotGoalMock() {
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Utility to generate timestamps
  const now = () => new Date().toISOString();

  // Utility to generate a random ID
  const randomId = () => Math.random().toString(36).substring(2, 10);

  // Mock fuzzy outputs
  const fuzzyGoalOutputs = [
    "Back (Rule: 2)",
    "Forward (Rule: 5)",
    "Light Right (Rule: 26)",
    "Rotate Left (Rule: 11)",
  ];

  const fuzzyHumanOutputs = [
    "Public / Forward (Rule: 26)",
    "Near / Back (Rule: 2)",
    "Personal / Right (Rule: 14)",
  ];

  // Create a single mock log entry
  const createMockLog = () => ({
    id: randomId(),
    label: Math.random() > 0.5 ? "Global Goal - Reached!" : "Intermediate Goal - Reached!",
    fuzzy_output_goal: fuzzyGoalOutputs[Math.floor(Math.random() * fuzzyGoalOutputs.length)],
    fuzzy_output_human: fuzzyHumanOutputs[Math.floor(Math.random() * fuzzyHumanOutputs.length)],
    timestamp: now(),
    feedback: "", // no feedback yet
  });

  useEffect(() => {
    setIsLoading(false);

    // Add initial mock logs
    setLogs([
      createMockLog(),
      createMockLog(),
      createMockLog(),
    ]);

    // Simulate new logs arriving every 100 seconds
    const interval = setInterval(() => {
      setLogs(prev => [createMockLog(), ...prev]);
    }, 100000);

    return () => clearInterval(interval);
  }, []);

  return { logs, isLoading };
}
