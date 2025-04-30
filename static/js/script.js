document.getElementById("resumeForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const resumeText = document.getElementById("resume").value.toLowerCase();
  const jdText = document.getElementById("jd").value.toLowerCase();

  const jdWords = new Set(jdText.match(/\b[a-z]{4,}\b/g)); // extract words of 4+ chars
  const resumeWords = new Set(resumeText.match(/\b[a-z]{4,}\b/g));

  const missingKeywords = [...jdWords].filter(word => !resumeWords.has(word));

  const topSuggestions = missingKeywords.slice(0, 10); // Show top 10

  const resultsDiv = document.getElementById("results");
  if (topSuggestions.length > 0) {
    resultsDiv.innerHTML = `
      <h3>Suggested Keywords to Add:</h3>
      <ul>${topSuggestions.map(word => `<li>${word}</li>`).join('')}</ul>
    `;
  } else {
    resultsDiv.innerHTML = "<p>Your resume already covers most keywords in the JD!</p>";
  }
});
