document.getElementById('resume-upload-form').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const resume = document.getElementById('resume').files[0];
    const jd = document.getElementById('jd').value;
  
    if (!resume || !jd) {
      alert('Please upload your resume and paste the job description.');
      return;
    }
  
    // Simulate a suggestion system
    alert('Resume submitted successfully!\n\nKeyword suggestions based on JD:\n- Leadership\n- Time Management\n- Python\n- Data Analysis');
  });
  