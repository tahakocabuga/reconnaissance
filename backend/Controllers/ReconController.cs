using System.Collections.Generic;
using System.Diagnostics;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using ReconAPI.Models;
using ReconAPI.Services;

namespace ReconAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ReconController : ControllerBase
    {
        [HttpPost("scan")]
public async Task<IActionResult> StartScan([FromBody] string url)
{
    Uri uri = new Uri(url);
    string host = uri.Host;
    var finalReconProcess = new Process
    {
        StartInfo = new ProcessStartInfo
        {
            FileName = "docker",
            Arguments = $"run --rm finalrecon --full {url}",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
        }
    };

    var subFinderProcess = new Process
    {
        StartInfo = new ProcessStartInfo
        {
            FileName = "docker",
            Arguments = $"run --rm projectdiscovery/subfinder:latest -d {url}",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
        }
    };
    
    var katanaProcess = new Process
    {
        StartInfo = new ProcessStartInfo
        {
            FileName = "docker",
            Arguments = $"run --rm projectdiscovery/katana -u {url}",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
        }
    };

    var naabuProcess = new Process
    {
        StartInfo = new ProcessStartInfo
        {
            FileName = "docker",
            Arguments = $"run --rm projectdiscovery/naabu -host {host}",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
        }
    };

    var finalReconTask = RunTool(finalReconProcess, url);
    var subFinderTask = RunTool(subFinderProcess, url);
    var katanaTask = RunTool(katanaProcess, url);
    var naabuTask = RunTool(naabuProcess, url);
    await Task.WhenAll(finalReconTask, subFinderTask, katanaTask, naabuTask);

    var finalReconResult = await finalReconTask;
    var subFinderResult = await subFinderTask;
    var katanaResult = await katanaTask;
    var naabuResult = await naabuTask;

    var mergedSubdomains = new HashSet<string>(finalReconResult.Subdomains);
    mergedSubdomains.UnionWith(subFinderResult.Subdomains);

    var reconResult = new ReconResult
    {
        WhoisInfo = finalReconResult.WhoisInfo,
        Subdomains = new List<string>(mergedSubdomains),
        Crawl = katanaResult.Crawl,
        Ports = naabuResult.Ports
    };

    return Ok(reconResult);
}



        private async Task<ReconResult> RunTool(Process process, string targetDomain)
        {
            process.Start();
            string output = await process.StandardOutput.ReadToEndAsync();
            string errorOutput = await process.StandardError.ReadToEndAsync();
            process.WaitForExit();

            if (!string.IsNullOrEmpty(errorOutput))
            {
                Console.WriteLine($"Error output: {errorOutput}");
            }

            var whoisInfo = new WhoisInfo
            {
                AsnRegistry = ExtractValue(output, @"\[\+\] asn_registry: (.*)"),
                Asn = ExtractValue(output, @"\[\+\] asn: (.*)"),
                AsnCidr = ExtractValue(output, @"\[\+\] asn_cidr: (.*)"),
                AsnCountryCode = ExtractValue(output, @"\[\+\] asn_country_code: (.*)"),
                AsnDate = ExtractValue(output, @"\[\+\] asn_date: (.*)"),
                AsnDescription = ExtractValue(output, @"\[\+\] asn_description: (.*)"),
                Query = ExtractValue(output, @"\[\+\] query: (.*)"),
                Cidr = ExtractValue(output, @"\[\+\] cidr: (.*)"),
                Name = ExtractValue(output, @"\[\+\] name: (.*)"),
                Handle = ExtractValue(output, @"\[\+\] handle: (.*)"),
                Range = ExtractValue(output, @"\[\+\] range: (.*)"),
                Description = ExtractValue(output, @"\[\+\] description: (.*)"),
                Country = ExtractValue(output, @"\[\+\] country: (.*)"),
                Address = ExtractValue(output, @"\[\+\] address: (.*)"),
                Created = ExtractValue(output, @"\[\+\] created: (.*)"),
                Updated = ExtractValue(output, @"\[\+\] updated: (.*)")
            };

            
            var subdomainRegex = new Regex(@"(?:^|\n)([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}\.(?:[a-zA-Z]{2,}|[a-zA-Z]{2}\.[a-zA-Z]{2}))");
            var subdomainMatches = subdomainRegex.Matches(output);
            var subdomains = new List<string>();

            foreach (Match match in subdomainMatches)
            {
                string subdomain = match.Value.Trim();
                if (!subdomains.Contains(subdomain))
                {
                    subdomains.Add(subdomain);
                }
            }

            var crawlRegex = new Regex(@"https?:\/\/[^\s]+");
            var crawlMatches = crawlRegex.Matches(output);
            var crawlResults = new List<string>();

            foreach (Match match in crawlMatches)
            {
                string link = match.Value.Trim();
                if (!crawlResults.Contains(link))
                {
                    crawlResults.Add(link);
                }
            }
            
            var naabuRegex = new Regex(@"(?:^|\n)([^:]+):(\d+)");
            var naabuMatches = naabuRegex.Matches(output);
            var openPorts = new List<string>();

            foreach (Match match in naabuMatches)
            {
                string port = $"{match.Groups[1].Value}:{match.Groups[2].Value}";
                if (!openPorts.Contains(port))
                {
                    openPorts.Add(port.Trim());
                }
            }

            var reconResult = new ReconResult
            {
                WhoisInfo = whoisInfo,
                Subdomains = subdomains,
                Crawl = crawlResults,
                Ports = openPorts
            };

            return reconResult;
        }

        private string? ExtractValue(string output, string regexPattern)
        {
            var match = Regex.Match(output, regexPattern);
            return match.Success ? match.Groups[1].Value : null;
        }
    }
}
