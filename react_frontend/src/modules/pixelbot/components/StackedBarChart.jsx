import React from 'react';
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

// StackedBarChart component
export default function StackedBarChart({ data, orientation = "horizontal", xAxisLabel, yAxisLabel }) {
    const hasData = data && ((data instanceof Map && data.size > 0) || (Array.isArray(data) && data.length > 0));

    if (!hasData) {
        return <div className="chart-empty">No data available</div>;
    }

    let series = [];
    let categories = [];

    if (data instanceof Map) {
        Array.from(data.entries()).forEach(([name, segments], index) => {
            series.push({
                name: name,
                data: segments.map(s => s.value),
                color: greenShades[index % greenShades.length]
            });
            if (index === 0) {
                categories = segments.map(s => s.label);
            }
        });
    } else if (Array.isArray(data)) {
        // Fallback for Array support (legacy)
        if (data[0]?.name) {
            series = data.map((s, index) => ({
                name: s.name,
                data: s.data,
                color: greenShades[index % greenShades.length]
            }));
            categories = Array.from({ length: data[0].data.length }, (_, i) => `Session ${i + 1}`);
        } else {
            series = [{
                name: 'Value',
                data: data.map(d => d.value),
                color: greenShades[2]
            }];
            categories = data.map(d => d.label);
        }
    }

    const options = {
        chart: {
            type: 'bar',    // Horizontal bar chart
            height: 200,
            backgroundColor: 'transparent'
        },
        title: {
            text: null
        },
        xAxis: {
            categories: categories, // X-axis categories
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
            }
        },
        legend: {
            enabled: true,
            align: 'center',
            verticalAlign: 'top',
            layout: 'horizontal',
            x: 0,
            y: 0
        },
        plotOptions: {
            bar: {
                stacking: 'normal', // Stack bars on top of each other
                borderRadius: 4
            }
        },
        series: series,
        credits: {
            enabled: false
        }
    };

    return <HighchartsReact highcharts={Highcharts} options={options} />;
}