import LoanIndexItem from "./LoanIndexItems";
import useToggle from "../../hooks/useToggle";

export default function LoanIndex({ loans, selectedLoanIndex, selectLoan, removeLoan }) {
  const { toggles, toggle } = useToggle({ loanIndexList: true });
  return (
    <ul class="list-group mt-2">
      <li class="list-group-item loan-index-head" onClick={() => toggle('loanIndexList')}>
        Loans
          <div class="float-right">
            {toggles.loanIndexList ? <OpenedCaret /> : <ClosedCaret />}
          </div>
      </li>
      {toggles.loanIndexList && loans.map((loan, index) => (
        <LoanIndexItem
          loan={loan}
          isSelected={index === selectedLoanIndex}
          selectLoan={() => selectLoan(index)}
          removeLoan={() => removeLoan(index)} />
      ))}
    </ul>
  );
}

const ClosedCaret = () => <svg fill="#000000" width="16" height="16" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M11.303 8l11.394 7.997L11.303 24z"/></svg>;
  
const OpenedCaret = () => <svg fill="#000000" width="16" height="16" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="M24 11.305l-7.997 11.39L8 11.305z"/></svg>;
