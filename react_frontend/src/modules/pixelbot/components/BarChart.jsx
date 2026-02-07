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
            type: 'column',
            height: 200,
            backgroundColor: 'transparent'
        },
        title: {
            text: null
        },
        xAxis: {
            categories: data.map(d => d.label.replace('Session ', 'S')),
            title: {
                text: xAxisLabel || null
            },
            labels: {
                style: {
                    fontSize: '11px',
                    color: '#666'
                }
            }
        },
        yAxis: {
            title: {
                text: yAxisLabel || null
            },
            labels: {
                style: {
                    fontSize: '11px',
                    color: '#666'
                }
            },
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
                color: greenShades[2], // Start with Medium Green
                borderRadius: 4,
                colorByPoint: true,
                colors: greenShades
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