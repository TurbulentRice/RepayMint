import { useEffect, useMemo, useRef, useState } from "preact/hooks";
import { getUserQueues } from "../../ajax";
import QueueAnalysis from "../QueueAnalysis";
import LoanChart from "./LoanChart";
import useToggle from "../../hooks/useToggle";
import QueueChart from "./QueueChart";
import LoanAnalysis from "../LoanAnalysis";
import ChartTabs from "./ChartTabs";

export default function LoanView({ loans, selectedLoanIndex, analysis }) {
  if (!loans.length) return <div> Add some loans to get started!</div>;

  const selectedLoan = loans[selectedLoanIndex];
  
  const [queues, setQueues] = useState({});
  const [method, setMethod] = useState('default');

  const combinedQueues = useMemo(() => ({...queues, default: {analysis, loans}}), [queues, loans, analysis]);

  const chartRef = useRef(null);
  const canvasRef = useRef(null);

  const { toggles, toggle } = useToggle({ loanView: false });
  
  useEffect(() => {
    (async () => {
      const userQueues = await getUserQueues();
      setQueues(userQueues);
    })();
  }, [loans]);

  return (
    <>

      {/* Tabs */}
      <ChartTabs isLoanView={!!toggles.loanView} toggleLoanView={() => toggle('loanView')} />

      {/* Chart */}
      {toggles.loanView
        ? <LoanChart selectedLoan={selectedLoan} canvasRef={canvasRef} chartRef={chartRef} />
        : <QueueChart queues={combinedQueues} method={method} canvasRef={canvasRef} chartRef={chartRef} />}

      {/* Analysis */}
      {toggles.loanView
        ? <LoanAnalysis loan={selectedLoan} />
        : <QueueAnalysis method={method} setMethod={setMethod} analysis={combinedQueues[method].analysis} selectedLoan={selectedLoan} />}

    </>
  );
}
