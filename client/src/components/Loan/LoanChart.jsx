export default function LoanChart({ canvasRef }) {
  return (
    <div class="row mt-2">
      <div class="chart-container">
        <canvas id="loanChart" ref={canvasRef}></canvas>
      </div>
    </div>
  );
}
