export default function ChartTabs({ isLoanView, toggleLoanView }) {
  return (
    <ul class="nav nav-tabs mt-2">
      <li class="nav-item">
        <button class={`nav-link${!isLoanView ? ' active' : ''}`} onClick={toggleLoanView}>Queue</button>
      </li>
      <li class="nav-item">
        <button class={`nav-link${isLoanView ? ' active' : ''}`} onClick={toggleLoanView}>Loan</button>
      </li>
    </ul>
  );
}
