import AudioAnalyzer from './components/AudioAnalyzer'

export default function App() {
  return (
    <div className="app-container">
      <header>
        <h1>VoiceGuard AI</h1>
        <p className="subtitle">Detect human vs synthetic voices in real-time</p>
      </header>
      <AudioAnalyzer />
      <footer className="footer">
        <p>Uses MFCCs and RandomForest classification</p>
      </footer>
    </div>
  )
}