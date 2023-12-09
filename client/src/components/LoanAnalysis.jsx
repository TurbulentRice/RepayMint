export default function LoanAnalysis({ loan }) {
  return (
    <div class="row border rounded p-2">
      <div class="col-6">
      <div class="row">
        <div class="col">
          <div><b>Starting balance:</b></div>
          <div><b>Interest rate:</b></div>
          <div><b>Payment amount:</b></div>
          <div><b>Duration:</b></div>
          <div><b>Number of payments:</b></div>
          <div><b>Principal paid:</b></div>
          <div><b>Interest paid:</b></div>
          <div><b>Total paid:</b></div>
          <div><b>Principal efficiency:</b></div>
        </div>
        <div class="col text-right">
          <div>{loan.startBalance}</div>
          <div>{loan.interestRate} %</div>
          <div>${loan.paymentAmt} / month</div>
          <div>{loan.analysis.duration} months</div>
          <div>{loan.analysis.numPayments}</div>
          <div>{loan.analysis.principalPaid}</div>
          <div>{loan.analysis.interestPaid}</div>
          <div>{loan.analysis.totalPaid}</div>
          <div>{loan.analysis.percentPrincipal}%</div>
        </div>
      </div>
      </div>
    </div>
  );
}
