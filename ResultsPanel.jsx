import { Doughnut } from 'react-chartjs-2'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

export default function ResultsPanel({ data }) {
  const chartData = {
    labels: ['Human', 'AI'],
    datasets: [{
      data: [data.confidence * 100, (1 - data.confidence) * 100],
      backgroundColor: ['#10b981', '#ef4444'],
      borderWidth: 0
    }]
  }

  return (
    <div className={`results ${data.is_human ? 'human' : 'ai'}`}>
      <h2>
        {data.is_human ? (
          <span className="result-good">✅ Genuine Human Voice</span>
        ) : (
          <span className="result-bad">🤖 AI-Generated Voice</span>
        )}
      </h2>
      <div className="chart-wrapper">
        <Doughnut data={chartData} />
        <div className="confidence-value">
          {(data.confidence * 100).toFixed(1)}%
        </div>
      </div>
      <p className="confidence-label">Confidence Score</p>
    </div>
  )
}