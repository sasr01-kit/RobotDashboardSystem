import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import { useState, useEffect, useMemo } from 'react';

export default function CalendarHeatMap({ id, data, startDate, endDate, colorScale, onPrint }) {
    const [heatmapLoaded, setHeatmapLoaded] = useState(false);

    useEffect(() => {
        import('highcharts/modules/heatmap').then((module) => {
            const heatmapModule = module.default || module;
            if (typeof heatmapModule === 'function') {
                heatmapModule(Highcharts);
            }
            setHeatmapLoaded(true);
        });
    }, []);

    // Configuration for the heatmap chart
    const options = useMemo(() => ({
        chart: {
            type: 'heatmap',
            height: 200,
            marginTop: 10,
            marginBottom: 50,
            marginLeft: 90,
            marginRight: 20,
            backgroundColor: 'transparent'
        },
        title: {
            text: null
        },
        xAxis: {
            visible: true,
            labels: {
                enabled: true,
                formatter: function () {
                    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
                    const weekIndex = this.value;

                    const weekData = data.filter(d => d.x === weekIndex);
                    if (weekData.length === 0) return '';

                    const firstDayOfWeek = weekData.reduce((earliest, current) => {
                        return current.date < earliest.date ? current : earliest;
                    });

                    const currentMonth = firstDayOfWeek.date.getMonth();

                    const prevWeekData = data.filter(d => d.x === weekIndex - 1);
                    if (prevWeekData.length === 0) {
                        return monthNames[currentMonth];
                    }

                    const prevWeekFirstDay = prevWeekData.reduce((earliest, current) => {
                        return current.date < earliest.date ? current : earliest;
                    });

                    const prevMonth = prevWeekFirstDay.date.getMonth();

                    if (currentMonth !== prevMonth) {
                        return monthNames[currentMonth];
                    }
                    return '';
                },
                style: {
                    fontSize: '12px',
                    color: '#666'
                },
                step: 1,
                rotation: 0
            },
            lineWidth: 0,
            tickLength: 0,
            tickInterval: 1
        },
        yAxis: {
            categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            title: null,
            reversed: true,
            labels: {
                style: {
                    fontSize: '11px',
                    color: '#666'
                }
            },
            gridLineWidth: 0
        },
        colorAxis: colorScale,
        legend: {
            enabled: false
        },
        tooltip: {
            formatter: function () {
                const point = this.point;
                const date = new Date(point.date);

                return `<b>${date.toLocaleDateString()}</b><br/>
                    Sessions: <b>${point.value}</b>`;
            },
            backgroundColor: 'rgba(0, 0, 0, 0.85)',
            borderWidth: 0,
            borderRadius: 8,
            style: {
                color: '#fff',
                fontSize: '12px'
            }
        },
        plotOptions: {
            heatmap: {
                borderWidth: 2,
                borderColor: '#fff',
                dataLabels: {
                    enabled: false
                },
                pointPadding: 0,
                colsize: 1,
                rowsize: 1
            }
        },
        series: [{
            name: 'Robot Usage',
            data: data
        }],
        credits: {
            enabled: false
        }
    }), [data, colorScale]);

    if (!heatmapLoaded) {
        return <div>Loading heatmap...</div>;
    }

    return (
        <div id={id} className="usage-history-card">
            <div className="usage-header">
                <h3>Robot Usage History</h3>
                <svg onClick={onPrint} className="print-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="6 9 6 2 18 2 18 9"></polyline>
                    <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                    <rect x="6" y="14" width="12" height="8"></rect>
                </svg>
            </div>
            <HighchartsReact
                highcharts={Highcharts}
                options={options}
            />
            <div className="heatmap-footer">
                <div className="heatmap-legend">
                    <span className="legend-label">{colorScale.dataClasses[0].name}</span>

                    {colorScale.dataClasses.map((dataClass, index) => (
                        <div key={index} className="legend-item" title={dataClass.name}>
                            <span className={`box box-${index}`} style={{ backgroundColor: dataClass.color }}></span>
                            <span>{dataClass.label}</span>
                        </div>
                    ))}

                    <span className="legend-label">{colorScale.dataClasses[colorScale.dataClasses.length - 1].name}</span>
                </div>
            </div>
        </div>
    );
}