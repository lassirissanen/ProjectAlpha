const baseUrl = process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:5000";

async function get(path, message, suggestion) {
  const url = `${baseUrl}${path}`;
  const data = {
    message: message,
    suggestion: suggestion,
  };
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify(data),
    });
    return response.json();
  } catch (error) {
    console.log(error);
  }
  return null;
}

async function getTensorflowClassification(message, suggestion) {
  const path = "/classify-1";
  return await get(path, message, suggestion);
}

async function getCombinedClassification(message, suggestion) {
  const path = "/classify-2";
  return await get(path, message, suggestion);
}

async function getOpenAIClassification(message, suggestion) {
  const path = "/classify-3";
  return await get(path, message, suggestion);
}

export {
  getTensorflowClassification,
  getCombinedClassification,
  getOpenAIClassification,
};
