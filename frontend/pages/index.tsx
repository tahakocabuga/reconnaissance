import Image from 'next/image';
import Head from 'next/head';

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-between min-h-screen p-24">
      <Head>
        <title>PentestScan - The Ultimate Web Reconnaissance and Penetration Testing Tool</title>
        <link rel="preconnect" href="https://fonts.gstatic.com" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet" />
      </Head>

      <header className="w-full max-w-5xl text-center lg:text-left">
        <h1 className="text-4xl font-semibold mb-6 font-mono">PentestScan</h1>
        <p className="text-gray-500 mb-6">The ultimate web reconnaissance and penetration testing tool.</p>
        <p className="text-gray-500 mb-6">With PentestScan, you can:</p>
        <ul className="text-gray-500 mb-6 list-disc list-inside">
          <li>Scan websites for vulnerabilities and weaknesses</li>
          <li>Perform automated and manual web application testing</li>
          <li>Discover hidden files and directories</li>
          <li>Enumerate subdomains and open ports</li>
        </ul>
        <a href="/recon" className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Get Started
        </a>
      </header>

      <div className="relative flex items-center">
        <Image
          src="/next.svg"
          alt="PentestScan Logo"
          width={180}
          height={180}
          priority={true}
        />
      </div>
    </main>
  );
}
