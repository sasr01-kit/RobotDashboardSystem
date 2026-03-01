import React, { useEffect, useState } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

const greenShades = [
    '#1B5E20', // Dark Green
    '#2E7D32',
    '#4CAF50', // Medium Green
    '#81C784',
    '#C8E6C9', // Light Green
    '#E8F5E9', '#A5D6A7', '#66BB6A', '#43A047', '#388E3C'
];

// A simple BarChart component using Highcharts
export default function BarChart({ data, color = '#20A090', xAxisLabel, yAxisLabel, averageLine }) {
    if (!data || data.length === 0) {
        return <div className="chart-empty">No data available</div>;
    }

    // Highcharts configuration
    const options = {
        chart: {
            type: 'column', // Use column chart type
            height: 200,    // Set chart height
            backgroundColor: 'transparent' // Transparent background
        },
        title: {
            text: null
        },
        xAxis: {
            categories: data.map(d => d.label.replace('Session ', 'S')), // Shorten labels
            title: {
                text: xAxisLabel || null // Optional X-axis title
            },
            labels: {
                style: {
                    fontSize: '11px', // Small font size
                    color: '#666'
                }
            }
        },
        yAxis: {
            title: {
                text: yAxisLabel || null // Optional Y-axis title
            },
            labels: {
                style: {
                    fontSize: '11px',
                    color: '#666'
                }
            },
            // Add a dashed red line for the average if provided
            plotLines: averageLine ? [{
                color: '#FF4444',
                width: 2,
                value: averageLine,
                dashStyle: 'Dash',
                label: {
                    text: `Average: ${averageLine.toFixed(1)}`,
                    align: 'right',
                    style: {
                        color: '#FF4444',
                        fontSize: '10px'
                    }
                },
                zIndex: 5
            }] : []
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            column: {
                color: greenShades[2], // Default color (Medium Green)
                borderRadius: 4,       // Rounded corners
                colorByPoint: true,    // Different color for each point
                colors: greenShades    // Use custom color palette
            }
        },
        series: [{
            name: yAxisLabel || 'Value',
            data: data.map(d => d.value)
        }],
        credits: {
            enabled: false
        }
    };

    return <HighchartsReact highcharts={Highcharts} options={options} />;
}