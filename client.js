const startBtn = document.getElementById("startBtn");
const transcriptEl = document.getElementById("transcript");
const statusEl = document.getElementById("status");

let ws;
let mediaRecorder;

startBtn.onclick = async () => {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    ws.close();
    startBtn.textContent = "Start Recognition";
    statusEl.textContent = "Stopped";
    return;
  }

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });

  ws = new WebSocket("ws://localhost:8000");

  ws.binaryType = "arraybuffer";

  ws.onopen = () => {
    transcriptEl.textContent = "";
    statusEl.textContent = "Connected and listening...";
    startBtn.textContent = "Stop Recognition";
    mediaRecorder.start(250); // send audio chunks every 250ms
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const { text, is_final } = data;
    if (is_final) {
      transcriptEl.textContent += text + "\n";
    } else {
      const lines = transcriptEl.textContent.split("\n");
      lines[lines.length - 1] = text;
      transcriptEl.textContent = lines.join("\n");
    }
  };

  mediaRecorder.ondataavailable = (event) => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(event.data);
    }
  };
};
