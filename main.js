const imageInput = document.getElementById("imageInput");
const predictBtn = document.getElementById("predictBtn");
const preview = document.getElementById("preview");
const resultBox = document.getElementById("resultBox");
const quality = document.getElementById("quality");
const defect = document.getElementById("defect");

imageInput.addEventListener("change", () => {
  const file = imageInput.files[0];
  if (file) {
    preview.src = URL.createObjectURL(file);
  }
});

predictBtn.addEventListener("click", async () => {
  const file = imageInput.files[0];
  if (!file) {
    resultBox.classList.remove("hidden");
    quality.textContent = "⚠️ Please upload an image first!";
    defect.textContent = "";
    return;
  }

  resultBox.classList.remove("hidden");
  quality.textContent = "⏳ Analyzing seed quality...";
  defect.textContent = "";

  const formData = new FormData();
  formData.append("image", file);

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData
    });

    let data;
    try {
      data = await response.json();
    } catch (err) {
      quality.textContent = "❌ Server returned invalid JSON.";
      defect.textContent = "";
      return;
    }

    if (!response.ok) {
      quality.textContent = `❌ Error: ${data.error || 'Server error'}`;
      defect.textContent = data.details ? `Details: ${data.details}` : "";
      return;
    }

    // ✅ Display results nicely
    quality.textContent = `🌾 Quality: ${data.quality}`;
    defect.textContent = `🧪 Defect Fraction: ${(data.defect_fraction * 100).toFixed(2)}%`;
  } catch (error) {
    quality.textContent = "❌ Prediction failed: " + error.message;
    defect.textContent = "";
  }
});
