import { useState, ChangeEvent, FormEvent } from "react";

const Recon = () => {
  const [url, setUrl] = useState("");
  const [subdomains, setSubdomains] = useState([]);
  const [crawl, setCrawl] = useState([]);
  const [ports, setPorts] = useState([]);
  const [whoisInfo, setWhoisInfo] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    let apiUrl = url;
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
      apiUrl = "http://" + apiUrl;
    }
    const response = await fetch("http://localhost:5223/api/recon/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(apiUrl),
    });
    setIsLoading(false);

    const result = await response.json();
    setSubdomains(result.subdomains);
    setCrawl(result.crawl);
    setPorts(result.ports);
    setWhoisInfo(result.whoisInfo);
  };
  

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUrl(e.target.value);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-gray-200">
      <h1 className="text-5xl font-bold mb-8 text-purple-600">Recon Tool</h1>
      <form onSubmit={handleSubmit} className="flex flex-col items-center justify-center w-full max-w-lg p-8 bg-gray-800 rounded-lg shadow-lg">
        <input
          type="text"
          value={url}
          onChange={handleInputChange}
          placeholder="Enter URL"
          required
          className="w-full px-4 py-2 mb-4 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600"
        />
        <button type="submit" className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-600">
          {isLoading ? (
            <svg className="animate-spin h-5 w-5 mr-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm12 0a8 8 0 100-16 8 8 0 000 16z" />
            </svg>
          ) : (
            "Start Scan"
          )}
        </button>
      </form>
      {subdomains.length > 0 && (
        <div className="w-full max-w-lg mt-8 bg-gray-800 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-4 text-purple-600 bg-gray-700 p-4 rounded-t-lg">Subdomains</h2>
          <pre className="p-4 whitespace-pre-wrap break-words">{subdomains.join("\n")}</pre>
        </div>
      )}
      {crawl.length > 0 && (
        <div className="w-full max-w-lg mt-8 bg-gray-800 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-4 text-purple-600 bg-gray-700 p-4 rounded-t-lg">Crawl</h2>
          <pre className="p-4 whitespace-pre-wrap break-words">{crawl.join("\n")}</pre>
        </div>
      )}
      {ports.length > 0 && (
        <div className="w-full max-w-lg mt-8 bg-gray-800 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-4 text-purple-600 bg-gray-700 p-4 rounded-t-lg">Ports</h2>
          <pre className="p-4 whitespace-pre-wrap break-words">{ports.join("\n")}</pre>
        </div>
      )}
      {Object.keys(whoisInfo).length > 0 && (
        <div className="w-full max-w-lg mt-8 bg-gray-800 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-4 text-purple-600 bg-gray-700 p-4 rounded-t-lg">Whois Info</h2>
        <div className="p-4 overflow-x-auto">
        <pre className="whitespace-pre-wrap break-words">{JSON.stringify(whoisInfo, null, 2)}</pre>
        </div>
        </div>
        )}
        </div>
        );
        };
        
        export default Recon;
