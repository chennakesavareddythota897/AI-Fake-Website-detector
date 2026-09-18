export async function scanWebsite(url) {
  const response = await fetch(
    `http://127.0.0.1:8000/scan?url=${encodeURIComponent(url)}`
  );
  const data = await response.json();
  return data;
}

export async function getHistory() {
  const response = await fetch("http://127.0.0.1:8000/history");
  const data = await response.json();
  return data;
}