using System.Text.RegularExpressions;
using ReconAPI.Models;

namespace ReconAPI.Services
{
    public class WhoisExtractor
    {
        public static WhoisInfo ExtractWhoisInfo(string input)
        {
            var whoisInfo = new WhoisInfo();
            var regexPattern = @"\[+] (\w+): (.+)";
            var matches = Regex.Matches(input, regexPattern);

            foreach (Match match in matches)
            {
                var key = match.Groups[1].Value;
                var value = match.Groups[2].Value;

                switch (key)
                {
                    case "asn_registry":
                        whoisInfo.AsnRegistry = value;
                        break;
                    case "asn":
                        whoisInfo.Asn = value;
                        break;
                    case "asn_cidr":
                        whoisInfo.AsnCidr = value;
                        break;
                    case "asn_country_code":
                        whoisInfo.AsnCountryCode = value;
                        break;
                    case "asn_date":
                        whoisInfo.AsnDate = value;
                        break;
                    case "asn_description":
                        whoisInfo.AsnDescription = value;
                        break;
                    case "query":
                        whoisInfo.Query = value;
                        break;
                    case "cidr":
                        whoisInfo.Cidr = value;
                        break;
                    case "name":
                        whoisInfo.Name = value;
                        break;
                    case "handle":
                        whoisInfo.Handle = value;
                        break;
                    case "range":
                        whoisInfo.Range = value;
                        break;
                    case "description":
                        whoisInfo.Description = value;
                        break;
                    case "country":
                        whoisInfo.Country = value;
                        break;
                    case "address":
                        whoisInfo.Address = value;
                        break;
                    case "created":
                        whoisInfo.Created = value;
                        break;
                    case "updated":
                        whoisInfo.Updated = value;
                        break;
                }
            }

            return whoisInfo;
        }
    }
}
