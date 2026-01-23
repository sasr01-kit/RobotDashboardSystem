import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

// LineChart component to render a line chart using Highcharts
const greenShades = [
    '#1B5E20', // Dark Green
    '#2E7D32',
    '#4CAF50', // Medium Green
    '#81C784',
    '#C8E6C9', // Light Green
    '#E8F5E9', '#A5D6A7', '#66BB6A', '#43A047', '#388E3C'
];

export default function LineChart({ data, lineColor = '#20A090', showGrid = true, xAxisLabel, yAxisLabel }) {
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
        if (data[0]?.name) {
            series = data.map((s, index) => ({
                name: s.name,
                data: s.data,
                color: greenShades[index % greenShades.length]
            }));
            categories = Array.from({ length: data[0].data.length }, (_, i) => `S${i + 1}`);
        } else {
            series = [{
                name: yAxisLabel || 'Value',
                data: data.map(d => d.value),
                color: greenShades[2]
            }];
            categories = data.map(d => d.label);
        }
    }

    // Configure chart options
    const options = {
        chart: {
            type: 'line',
            height: 200,
            backgroundColor: 'transparent'
        },
        title: {
            text: null
        },
        xAxis: {
            categories: categories,
            title: {
                text: xAxisLabel || null
            },
            gridLineWidth: showGrid ? 1 : 0,
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
            gridLineWidth: showGrid ? 1 : 0,
            labels: {
                style: {
                    fontSize: '11px',
                    color: '#666'
                }
            }
        },
        legend: {
            enabled: series.length > 1,
            align: 'center',
            verticalAlign: 'top',
            layout: 'horizontal',
            y: 0
        },
        plotOptions: {
            line: {
                marker: {
                    enabled: true,
                    radius: 4
                }
            }
        },
        series: series,
        credits: {
            enabled: false
        }
    };

    return <HighchartsReact highcharts={Highcharts} options={options} />;
}