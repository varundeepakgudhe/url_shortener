async function shortenUrl() {
    const urlInput = document.getElementById("urlInput").value;
    const result = document.getElementById("result");
  
    if (!urlInput) {
      result.innerText = "Please enter a URL";
      return;
    }
  
    try {
      const response = await fetch("http://127.0.0.1:8001/api/shorten", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ original_url: urlInput })
      });
  
      const data = await response.json();
  
      if (!response.ok) {
        result.innerText = "Error creating short URL";
        return;
      }
  
      const shortUrl = `http://127.0.0.1:8001/${data.short_code}`;
      result.innerHTML = `Short URL: <a href="${shortUrl}" target="_blank">${shortUrl}</a>`;
    } catch (error) {
      result.innerText = "Backend not reachable";
    }
  }