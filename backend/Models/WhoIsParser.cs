using ReconAPI.Models;
using System.Text.RegularExpressions;

namespace ReconAPI.Parser
{
    public class WhoisParser
    {
        public WhoisInfo ExtractWhoisInfo(string whoisText)
        {
            var whoisInfo = new WhoisInfo
            {
                // Add the additional fields similarly using regex
                AsnRegistry = ExtractValue(whoisText, @"\[\+\] asn_registry: (.*)"),
                Asn = ExtractValue(whoisText, @"\[\+\] asn: (.*)"),
                AsnCidr = ExtractValue(whoisText, @"\[\+\] asn_cidr: (.*)"),
                AsnCountryCode = ExtractValue(whoisText, @"\[\+\] asn_country_code: (.*)"),
                AsnDate = ExtractValue(whoisText, @"\[\+\] asn_date: (.*)"),
                AsnDescription = ExtractValue(whoisText, @"\[\+\] asn_description: (.*)"),
                Query = ExtractValue(whoisText, @"\[\+\] query: (.*)"),
                Cidr = ExtractValue(whoisText, @"\[\+\] cidr: (.*)"),
                Name = ExtractValue(whoisText, @"\[\+\] name: (.*)"),
                Handle = ExtractValue(whoisText, @"\[\+\] handle: (.*)"),
                Range = ExtractValue(whoisText, @"\[\+\] range: (.*)"),
                Description = ExtractValue(whoisText, @"\[\+\] description: (.*)"),
                Country = ExtractValue(whoisText, @"\[\+\] country: (.*)"),
                Address = ExtractValue(whoisText, @"\[\+\] address: (.*)"),
                Created = ExtractValue(whoisText, @"\[\+\] created: (.*)"),
                Updated = ExtractValue(whoisText, @"\[\+\] updated: (.*)")
            };

            return whoisInfo;
        }

        private string? ExtractValue(string input, string pattern)
        {
            var match = Regex.Match(input, pattern);
            return match.Success ? match.Groups[1].Value : null;
        }
    }
}
