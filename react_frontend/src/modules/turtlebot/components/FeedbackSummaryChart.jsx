import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import { useTurtlebotFeedback } from "../hooks/useTurtlebotFeedback"; 

// Component to display a pie chart summarizing the ratio of good vs bad feedback using the Highcharts library
export const FeedbackSummaryChart = () => {
  const { feedbackSummaryDTO } = useTurtlebotFeedback();
  
  const good = feedbackSummaryDTO?.goodRatio ?? 0;
  const bad = feedbackSummaryDTO?.badRatio ?? 0;


  const options = {
    chart: {
      type: "pie",
      backgroundColor: "transparent"
    },

    title: {
      text: null
    },

    tooltip: {
      pointFormat: "<b>{point.percentage:.1f}%</b>"
    },

    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: "pointer",
        dataLabels: {
          enabled: false
        }
      }
    },

    series: [
      {
        name: "Feedback",
        colorByPoint: true,
        data: [
          {
            name: "GOOD",
            y: good,
            color: "var(--success-green)"
          },
          {
            name: "BAD",
            y: bad,
            color: "var(--error-red)"
          }
        ]
      }
    ]
  };

  return <HighchartsReact highcharts={Highcharts} options={options} />;
};
