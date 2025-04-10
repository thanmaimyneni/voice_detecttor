// src/components/AudioAnalyzer.jsx
import { useState, useRef } from 'react';
import { Mp3Recorder } from 'mic-recorder-to-mp3';
import Wavesurfer from 'wavesurfer.js';

export default function AudioAnalyzer() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState('');
  const recorder = useRef(new Mp3Recorder());
  const waveformRef = useRef(null);

  const startRecording = async () => {
    try {
      await recorder.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Recording error:', error);
    }
  };

  const stopRecording = async () => {
    try {
      const [buffer, blob] = await recorder.current.stop().getMp3();
      setIsRecording(false);

      // Create audio URL
      const newAudioUrl = URL.createObjectURL(blob);
      setAudioUrl(newAudioUrl);

      // Initialize waveform
      if (waveformRef.current) {
        waveformRef.current.destroy();
      }
      waveformRef.current = Wavesurfer.create({
        container: '#waveform',
        waveColor: '#2563eb',
        progressColor: '#1e40af'
      });
      waveformRef.current.load(newAudioUrl);

      // Send to backend
      const formData = new FormData();
      formData.append('file', blob, 'recording.mp3');

      const response = await fetch('http://localhost:8000/detect', {
        method: 'POST',
        body: formData
      });

      setResult(await response.json());
    } catch (error) {
      console.error('Recording stop error:', error);
    }
  };

  return (
    <div className="analyzer">
      <button
        onClick={isRecording ? stopRecording : startRecording}
        className={isRecording ? 'stop-btn' : 'start-btn'}
      >
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>

      <div id="waveform" style={{ marginTop: '20px', height: '100px' }} />

      {audioUrl && (
        <audio controls src={audioUrl} style={{ marginTop: '10px' }} />
      )}
    </div>
  );
}