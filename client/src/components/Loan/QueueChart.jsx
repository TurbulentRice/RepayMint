import Chart from 'chart.js/auto';
import { useEffect } from 'preact/hooks';

export default function QueueChart({ queues, method, canvasRef, chartRef }) {
  useEffect(() => {
    const userLoans = queues[method].loans;
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
    <div class="row mt-2">
      <div class="chart-container">
        <canvas id="loanChart" ref={canvasRef}></canvas>
      </div>
    </div>
  );
}