import LoanIndexItem from "./LoanIndexItems";

export default function LoanIndex({ loans, selectedLoanIndex, selectLoan, removeLoan }) {
  return (
    <ul class="list-group">
      {loans.map((loan, index) => (
        <LoanIndexItem
          loan={loan}
          isSelected={index === selectedLoanIndex}
          selectLoan={selectLoan}
          removeLoan={removeLoan}
          index={index} />
      ))}
    </ul>
  );
}
