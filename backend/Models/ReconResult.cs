using System.Collections.Generic;

namespace ReconAPI.Models
{
    public class ReconResult
    {
        public List<string>? Subdomains { get; set; }
        public WhoisInfo? WhoisInfo { get; set; }
        public List<string>? Crawl { get; set; }
        public List<string>? Ports { get; set; }
    }
}
