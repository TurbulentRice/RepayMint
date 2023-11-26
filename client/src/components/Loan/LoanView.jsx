import { useEffect, useRef, useState } from "preact/hooks";
import Chart from 'chart.js/auto';
import { getUserQueues } from "../../ajax";

export default function LoanView({ loans }) {
  if (!loans) return <div></div>;
  
  const [queues, setQueues] = useState();
  const [method, setMethod] = useState('avalanche');

  const chartRef = useRef(null);
  const canvasRef = useRef(null);
  
  useEffect(() => {
    (async () => {
      const userQueues = await getUserQueues();
      setQueues(userQueues);
    })();
  }, [loans]);
  
  console.log('QUEUES:', queues)

  useEffect(() => {
    const userLoans = queues ? queues[method] : loans;
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

  const handle = (e) => {
    console.log('Repayment method:', e.target.value)
    setMethod(e.target.value);
  };

  return (
    <>
      <div class="row">
      </div>
      <div class="chart-container">
        <canvas id="loanChart" ref={canvasRef}></canvas>
      </div>
        <div class="col-4">
        <select name="repaymentMethod" onChange={handle} class="form-control">
          <option value="avalanche">Avalanche</option>
          <option value="blizzard">Blizzard</option>
          <option value="cascade">Cascade</option>
          <option value="iceSlide">Ice Slide</option>
          <option value="snowball">Snowball</option>
        </select>
      </div>
    </>
  );
}
