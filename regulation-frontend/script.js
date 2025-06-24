document.addEventListener("DOMContentLoaded", () => {
  const title = document.getElementById("pageTitle").innerText;
  const img = document.getElementById("bottomImage");

  if (title.includes("Regulation")) {
    img.src = "assets/6181711.jpg"; // 박스 검색 아이콘
  } else if (title.includes("Doc")) {
    img.src = "assets/Checklist.jpg"; // 체크리스트 이미지
  }

  const searchBtn = document.getElementById("searchBtn");
  if (searchBtn) {
    searchBtn.addEventListener("click", async () => {
      const country = document.getElementById("country").value;
      const cargoType = document.getElementById("cargoType").value;
      const resultBox = document.getElementById("resultBox");
      const errorBox = document.getElementById("errorBox");

      try {
        const res = await fetch(`http://localhost:9100/regulations/?country=${country}&cargo_type=${cargoType}`);
        if (!res.ok) throw new Error("No data found");
        const data = await res.json();

        errorBox.innerText = "";
        resultBox.innerHTML = `
          <p><strong>Country:</strong> ${data.country}</p>
          <p><strong>Cargo Type:</strong> ${data.cargo_type}</p>
          <p><strong>Documents:</strong> ${data.required_documents.join(", ")}</p>
          <p><strong>Packaging:</strong> ${data.packaging_requirement}</p>
          <p><strong>CO Required:</strong> ${data.co_required ? "Yes" : "No"}</p>
          <p><strong>Notes:</strong> ${data.notes}</p>
        `;
      } catch (err) {
        errorBox.innerText = "❌ No data found";
        resultBox.innerHTML = "";
      }
    });
  }
});
