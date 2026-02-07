import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import { useState, useEffect, useMemo } from 'react';

export default function CalendarHeatMap({ id, data, startDate, endDate, onPrint }) {
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
        colorAxis: { // Can be changed to a more suitable value range if needed
            dataClasses: [
                {
                    from: 0,
                    to: 0,
                    color: '#ebedf0',
                    name: 'No usage'
                },
                {
                    from: 1,
                    to: 2,
                    color: '#c6e48b',
                    name: 'Low'
                },
                {
                    from: 3,
                    to: 5,
                    color: '#7bc96f',
                    name: 'Medium'
                },
                {
                    from: 6,
                    to: 8,
                    color: '#239a3b',
                    name: 'High'
                },
                {
                    from: 9,
                    to: 999,
                    color: '#196127',
                    name: 'Intense'
                }
            ]
        },
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
    }), [data]);

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
                    <span className="legend-label">No usage</span>

                    <div className="legend-item" title="No usage">
                        <span className="box box-0"></span>
                        <span>0</span>
                    </div>

                    <div className="legend-item" title="Low">
                        <span className="box box-1"></span>
                        <span>1–2</span>
                    </div>

                    <div className="legend-item" title="Medium">
                        <span className="box box-2"></span>
                        <span>3–5</span>
                    </div>

                    <div className="legend-item" title="High">
                        <span className="box box-3"></span>
                        <span>6–8</span>
                    </div>

                    <div className="legend-item" title="Intense">
                        <span className="box box-4"></span>
                        <span>9+</span>
                    </div>

                    <span className="legend-label">Intense</span>
                </div>
            </div>
        </div>
    );
}