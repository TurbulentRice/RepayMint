export default function LoanView({ loan }) {
  if (!loan) return <div></div>;

  // Otherwise, make a solved Loan to display
  // Depending on Tool toggle, this can 
  // const loanToDisplay = loan.solveInPlace();

  // // Takes a Loan object, makes traces
  // const makeLoanTrace = loan => [{
  //   x: [...loan.paymentHistory.paymentNum],
  //   y: [...loan.paymentHistory.balance],
  // }]

  return (
    <div>
      <div class="row">
        {Object.entries(loan).map(([key, value], index) => key !== "paymentHistory" ? <p key={index}>{key}: {value}</p> : null)}
      </div>

      {/* <LinePlot plotData={makeLoanTrace(loanToDisplay)}/>   */}
        
    </div>
  );
}
