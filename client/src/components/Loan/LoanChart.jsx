import Chart from 'chart.js/auto';
import { useEffect } from "preact/hooks";

export default function LoanChart({ selectedLoan, canvasRef, chartRef }) {
  useEffect(() => {
    chartRef.current = new Chart(canvasRef.current, {
      type: 'line',
      options: {
        responsive: true
      }
    });
    chartRef.current.data.labels = selectedLoan.paymentHistory.pay_no;
    chartRef.current.data.datasets.push({
      label: selectedLoan.title,
      data: selectedLoan.paymentHistory.balance,
      borderWidth: 1
    });
    chartRef.current.update();
    return () => chartRef.current.destroy();
  }, [selectedLoan]);
  return (
    <div class="row mt-2">
      <div class="chart-container">
        <canvas id="loanChart" ref={canvasRef}></canvas>
      </div>
    </div>
  );
}
