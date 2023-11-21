import LoanIndexItem from "./LoanIndexItems";

export default function LoanIndex({ loans, selectLoan, removeLoan }) {
  return (
    <ul class="list-group">
      {loans.map((loan, index) => (
        <LoanIndexItem
          loan={loan}
          selectLoan={selectLoan}
          removeLoan={removeLoan}
          index={index} />
      ))}
    </ul>
  );
}
