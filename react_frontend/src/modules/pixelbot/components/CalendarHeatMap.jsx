import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import { useState, useEffect, useMemo } from 'react';

export default function CalendarHeatMap({ id, data, colorScale, onPrint }) {
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


    // Helper: Add color/name/label based on percentage buckets
    function enrichDataClasses(rawClasses) {
        if (!rawClasses) return [];
        return rawClasses.map((cls, index) => {
            const { from, to } = cls;


            // derive name by bucket position
            const names = ["No usage", "Low", "Medium", "High", "Intense"];
            const safeName = names[index] || `Level ${index + 1}`;

            // derive label directly from from–to
            const label = from === to ? `${from}` : `${from}–${to}`;

            // derive color dynamically
            const colors = ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"];
            const color = colors[index] || "#196127";

            return { ...cls, color, safeName, label };
        });
    }



    // Memoize enriched color scale to prevent recalculation
    const enrichedColorScale = useMemo(() => ({
        dataClasses: enrichDataClasses(colorScale?.dataClasses || [])
    }), [colorScale]);



    // Configuration for the heatmap chart
    const options = useMemo(() => ({
        chart: {
            type: 'heatmap',
            height: 200,
            marginTop: 10,
            marginBottom: 50,
            marginLeft: 90, // Space for Y-axis labels
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
                // Custom formatter to show month names based on week index
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
            categories: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], // Days of week
            title: null,
            reversed: true, // Show Monday at top
            labels: {
                style: {
                    fontSize: '11px',
                    color: '#666'
                }
            },
            gridLineWidth: 0
        },

        colorAxis: {
            dataClasses: enrichedColorScale.dataClasses,
        },

        legend: {
            enabled: false
        },
        tooltip: {
            // Custom tooltip to show date and value
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
                borderWidth: 2,     // Gap between cells
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
    }), [data, enrichedColorScale]);

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
                    {enrichedColorScale.dataClasses.map((dataClasses, index) => (
                        <div key={index} className="legend-item" title={dataClasses.safeName}>
                            <span className="legend-label">{dataClasses.safeName}</span>
                            <span className={`box box-${index}`} style={{ backgroundColor: dataClasses.color }}></span>
                            <span>{dataClasses.label}</span>
                        </div>
                    ))}

                </div>
            </div>
        </div>
    );
}