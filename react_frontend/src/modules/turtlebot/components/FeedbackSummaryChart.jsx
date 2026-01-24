import Highcharts, { width } from "highcharts";
import HighchartsReact from "highcharts-react-official";
import { useTurtlebotFeedback } from "../Hooks/useTurtlebotFeedback"; 
import { useTurtlebotFeedbackMock } from "../Hooks/useTurtlebotFeedbackMock";

export const FeedbackSummaryChart = () => {
  const { feedbackSummaryDTO } = useTurtlebotFeedbackMock();

  const good = feedbackSummaryDTO.goodRatio || 0;
  const bad = feedbackSummaryDTO.badRatio || 0;

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
