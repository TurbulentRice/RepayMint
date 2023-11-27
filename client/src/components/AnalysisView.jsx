export default function AnalysisView({ method, setMethod, analysis }) {
  return (
    <div class="row border rounded p-2">
      <div class="col-6">
        <div class="row">
          <select
            name="repaymentMethod"
            value={method}
            onChange={(e) => setMethod(e.target.value)} class="form-control">
            <option value="default">Default</option>
            <option value="avalanche">Avalanche</option>
            <option value="blizzard">Blizzard</option>
            <option value="cascade">Cascade</option>
            <option value="iceSlide">Ice Slide</option>
            <option value="snowball">Snowball</option>
          </select>
        </div>
      <div class="row">
        <div class="col">
          <div><b>Duration:</b></div>
          <div><b>Number of payments:</b></div>
          <div><b>Principal paid:</b></div>
          <div><b>Interest paid:</b></div>
          <div><b>Total paid:</b></div>
          <div><b>Principal efficiency:</b></div>
        </div>
        <div class="col text-right">
          <div>{analysis.duration} months</div>
          <div>{analysis.numPayments}</div>
          <div>{analysis.principalPaid}</div>
          <div>{analysis.interestPaid}</div>
          <div>{analysis.totalPaid}</div>
          <div>{analysis.percentPrincipal}%</div>
        </div>
      </div>
      </div>
    </div>
  );
}
