import { useEffect, useRef, useState } from "preact/hooks";
import Chart from 'chart.js/auto';
import { getUserQueues } from "../../ajax";
import AnalysisView from "../AnalysisView";
import LoanChart from "./LoanChart";

export default function LoanView({ loans, analysis }) {
  if (!loans) return <div> Add some loans to get started!</div>;
  
  const [queues, setQueues] = useState({});
  const [method, setMethod] = useState('default');

  const chartRef = useRef(null);
  const canvasRef = useRef(null);
  
  useEffect(() => {
    (async () => {
      const userQueues = await getUserQueues();
      console.log('FETCHED QUEUES:', userQueues)
      setQueues(userQueues);
    })();
  }, [loans]);
  
  useEffect(() => {
    const userLoans = queues[method]?.loans || loans;
    console.log('Making new chart for loans:', userLoans)
    chartRef.current = new Chart(canvasRef.current, {
      type: 'line',
      options: {
        responsive: true
      }
    });
    userLoans.forEach((loan) => {
      if (chartRef.current.data.labels.length < loan.paymentHistory.pay_no.length) {
        chartRef.current.data.labels = loan.paymentHistory.pay_no;
      }
      chartRef.current.data.datasets.push({
        label: loan.title,
        data: loan.paymentHistory.balance,
        borderWidth: 1
      });
    });
    chartRef.current.update();
    return () => chartRef.current.destroy();
  }, [queues, method]);

  return (
    <>

      {/* Chart */}
      <LoanChart canvasRef={canvasRef} />

      {/* Analysis */}
      <AnalysisView method={method} setMethod={setMethod} analysis={queues[method]?.analysis || analysis} />

    </>
  );
}
