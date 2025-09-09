console.log("🚀 Advanced script.js loaded!");

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const fileNameElem = document.getElementById("file-name");
const summaryLength = document.getElementById("summary-length");
const submitBtn = document.getElementById("submit-btn");
const extractedTextElem = document.getElementById("extracted-text");
const summaryElem = document.getElementById("summary");
const errorMsg = document.getElementById("error-msg");
const downloadBtn = document.getElementById("download-btn");

let selectedFile = null;

// Click → open file picker
dropZone.addEventListener("click", () => {
  console.log("Drop zone clicked");
  fileInput.click();
});

// File selected
fileInput.addEventListener("change", (e) => {
  selectedFile = e.target.files[0];
  console.log("File selected:", selectedFile);
  fileNameElem.textContent = selectedFile ? selectedFile.name : "No file selected";
});

// Drag & Drop
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});
dropZone.addEventListener("dragleave", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
});
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  if (e.dataTransfer.files.length > 0) {
    selectedFile = e.dataTransfer.files[0];
    console.log("File dropped:", selectedFile);
    fileNameElem.textContent = selectedFile.name;
  }
});

// ✅ Highlight important keywords dynamically (from backend)
function highlightKeywords(text, keywords) {
  if (!keywords || keywords.length === 0) return text;
  let highlighted = text;
  keywords.forEach((word) => {
    const regex = new RegExp(`\\b${word}\\b`, "gi");
    highlighted = highlighted.replace(regex, `<span class="highlight">${word}</span>`);
  });
  return highlighted;
}

// Download summary as text file
function downloadSummary(summaryText) {
  const blob = new Blob([summaryText], { type: "text/plain" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "summary.txt";
  link.click();
}

// Summarize button
submitBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    errorMsg.textContent = "⚠️ Please select a file first!";
    return;
  }

  errorMsg.textContent = "";
  extractedTextElem.innerHTML = '<div class="spinner"></div>';
  summaryElem.innerHTML = '<div class="spinner"></div>';
  downloadBtn.style.display = "none";

  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("summary_length", summaryLength.value);

  try {
    const response = await fetch("http://127.0.0.1:8000/upload/", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("Backend JSON:", data);

    if (response.ok) {
      extractedTextElem.textContent = data.extracted_text
        ? data.extracted_text.slice(0, 1000) + (data.extracted_text.length > 1000 ? "..." : "")
        : "⚠️ No text extracted.";

      // ✅ use backend keywords instead of static list
      const highlightedSummary = highlightKeywords(data.summary || "", data.keywords);
      summaryElem.innerHTML = highlightedSummary || "⚠️ No summary generated.";

      if (data.summary) {
        downloadBtn.style.display = "block";
        downloadBtn.onclick = () => downloadSummary(data.summary);
      }
    } else {
      errorMsg.textContent = data.error || "⚠️ Something went wrong!";
      extractedTextElem.textContent = "";
      summaryElem.textContent = "";
    }
  } catch (err) {
    console.error("Fetch error:", err);
    errorMsg.textContent = "⚠️ Cannot connect to backend!";
    extractedTextElem.textContent = "";
    summaryElem.textContent = "";
  }
});
