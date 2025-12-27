import { useState } from 'react';
import Head from 'next/head';

export default function Landing() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('/api/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        setSubmitted(true);
      } else {
        alert('Error signing up. Please try again.');
      }
    } catch (error) {
      console.error('Signup error:', error);
      alert('Error signing up. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>DeepfakeGuard - AI-Powered Deepfake Detection API</title>
        <meta name="description" content="Protect your community from deepfakes with our AI-powered detection API. Built for Telegram, Discord, and NFT marketplaces." />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        {/* Navigation */}
        <nav className="bg-black bg-opacity-50 backdrop-blur-md border-b border-purple-500/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-2">
                <span className="text-3xl">🛡️</span>
                <span className="text-2xl font-bold text-white">DeepfakeGuard</span>
              </div>
              <div className="flex space-x-6">
                <a href="#features" className="text-gray-300 hover:text-white transition">Features</a>
                <a href="#pricing" className="text-gray-300 hover:text-white transition">Pricing</a>
                <a href="#docs" className="text-gray-300 hover:text-white transition">API Docs</a>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6">
              Stop Deepfakes.<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
                Protect Your Community.
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              AI-powered deepfake detection API built for Telegram/Discord moderators and NFT marketplaces. 
              Detect manipulated media in seconds with webhook notifications.
            </p>

            {submitted ? (
              <div className="bg-green-500/20 border border-green-500/50 rounded-lg p-6 max-w-md mx-auto">
                <p className="text-green-400 text-lg font-semibold">✅ Check your email!</p>
                <p className="text-gray-300 mt-2">We've sent your API key and integration guide to {email}</p>
              </div>
            ) : (
              <form onSubmit={handleSignup} className="max-w-md mx-auto">
                <div className="flex flex-col sm:flex-row gap-3">
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="your@email.com"
                    required
                    className="flex-1 px-6 py-4 rounded-lg bg-white/10 border border-purple-500/50 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-pink-700 transition disabled:opacity-50"
                  >
                    {loading ? 'Processing...' : 'Get 10 Free Scans'}
                  </button>
                </div>
                <p className="text-gray-400 text-sm mt-3">No credit card required • Instant API key</p>
              </form>
            )}
          </div>
        </div>

        {/* Social Proof */}
        <div className="bg-black/30 py-8 border-y border-purple-500/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <p className="text-center text-gray-400 mb-4">Trusted by moderators protecting</p>
            <div className="flex justify-center items-center space-x-12 text-gray-500">
              <div className="text-center">
                <p className="text-3xl font-bold text-white">50K+</p>
                <p className="text-sm">Discord Members</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-white">25K+</p>
                <p className="text-sm">Telegram Users</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-white">10+</p>
                <p className="text-sm">NFT Marketplaces</p>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div id="features" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <h2 className="text-4xl font-bold text-white text-center mb-12">Why DeepfakeGuard?</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white/5 backdrop-blur-sm border border-purple-500/30 rounded-xl p-8 hover:border-purple-500/60 transition">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-bold text-white mb-3">Lightning Fast</h3>
              <p className="text-gray-300">Get deepfake detection results in under 3 seconds via simple REST API</p>
            </div>

            <div className="bg-white/5 backdrop-blur-sm border border-purple-500/30 rounded-xl p-8 hover:border-purple-500/60 transition">
              <div className="text-4xl mb-4">🔔</div>
              <h3 className="text-xl font-bold text-white mb-3">Webhook Notifications</h3>
              <p className="text-gray-300">Instant webhooks to your endpoint when deepfakes are detected</p>
            </div>

            <div className="bg-white/5 backdrop-blur-sm border border-purple-500/30 rounded-xl p-8 hover:border-purple-500/60 transition">
              <div className="text-4xl mb-4">👁️</div>
              <h3 className="text-xl font-bold text-white mb-3">Manual Review</h3>
              <p className="text-gray-300">Human experts review flagged content before final verdict</p>
            </div>

            <div className="bg-white/5 backdrop-blur-sm border border-purple-500/30 rounded-xl p-8 hover:border-purple-500/60 transition">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold text-white mb-3">High Accuracy</h3>
              <p className="text-gray-300">95%+ accuracy on deepfake videos and images with AI models</p>
            </div>

            <div className="bg-white/5 backdrop-blur-sm border border-purple-500/30 rounded-xl p-8 hover:border-purple-500/60 transition">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-bold text-white mb-3">Privacy First</h3>
              <p className="text-gray-300">Your media is analyzed and deleted. We never store content</p>
            </div>

            <div className="bg-white/5 backdrop-blur-sm border border-purple-500/30 rounded-xl p-8 hover:border-purple-500/60 transition">
              <div className="text-4xl mb-4">🔌</div>
              <h3 className="text-xl font-bold text-white mb-3">Easy Integration</h3>
              <p className="text-gray-300">Simple REST API with SDKs for Python, Node.js, and JavaScript</p>
            </div>
          </div>
        </div>

        {/* Pricing Section */}
        <div id="pricing" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <h2 className="text-4xl font-bold text-white text-center mb-4">Simple, Transparent Pricing</h2>
          <p className="text-gray-400 text-center mb-12">Start free, scale as you grow</p>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {/* Free Tier */}
            <div className="bg-white/5 backdrop-blur-sm border border-purple-500/30 rounded-xl p-8">
              <h3 className="text-2xl font-bold text-white mb-2">Free</h3>
              <p className="text-gray-400 mb-6">Get started</p>
              <div className="mb-6">
                <span className="text-5xl font-bold text-white">$0</span>
                <span className="text-gray-400">/month</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center text-gray-300">
                  <span className="text-green-500 mr-2">✓</span>{' '}
                  10 scans included
                </li>
                <li className="flex items-center text-gray-300">
                  <span className="text-green-500 mr-2">✓</span>{' '}
                  Webhook notifications
                </li>
                <li className="flex items-center text-gray-300">
                  <span className="text-green-500 mr-2">✓</span>{' '}
                  Email support
                </li>
                <li className="flex items-center text-gray-400">
                  <span className="text-gray-600 mr-2">✗</span>{' '}
                  No manual review
                </li>
              </ul>
              <button className="w-full py-3 border border-purple-500 text-purple-400 rounded-lg hover:bg-purple-500/10 transition">
                Start Free
              </button>
            </div>

            {/* Pro Tier */}
            <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 backdrop-blur-sm border-2 border-purple-500 rounded-xl p-8 transform scale-105">
              <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white text-xs font-bold px-3 py-1 rounded-full inline-block mb-3">
                MOST POPULAR
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Pro</h3>
              <p className="text-gray-300 mb-6">For growing communities</p>
              <div className="mb-6">
                <span className="text-5xl font-bold text-white">$49</span>
                <span className="text-gray-300">/month</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center text-gray-200">
                  <span className="text-green-400 mr-2">✓</span>{' '}
                  500 scans/month
                </li>
                <li className="flex items-center text-gray-200">
                  <span className="text-green-400 mr-2">✓</span>{' '}
                  Manual review on flagged content
                </li>
                <li className="flex items-center text-gray-200">
                  <span className="text-green-400 mr-2">✓</span>{' '}
                  Priority webhooks
                </li>
                <li className="flex items-center text-gray-200">
                  <span className="text-green-400 mr-2">✓</span>{' '}
                  24/7 support
                </li>
              </ul>
              <button className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-lg hover:from-purple-700 hover:to-pink-700 transition">
                Get Started
              </button>
            </div>

            {/* Enterprise Tier */}
            <div className="bg-white/5 backdrop-blur-sm border border-purple-500/30 rounded-xl p-8">
              <h3 className="text-2xl font-bold text-white mb-2">Enterprise</h3>
              <p className="text-gray-400 mb-6">For large platforms</p>
              <div className="mb-6">
                <span className="text-5xl font-bold text-white">Custom</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center text-gray-300">
                  <span className="text-green-500 mr-2">✓</span>{' '}
                  Unlimited scans
                </li>
                <li className="flex items-center text-gray-300">
                  <span className="text-green-500 mr-2">✓</span>{' '}
                  Dedicated manual review team
                </li>
                <li className="flex items-center text-gray-300">
                  <span className="text-green-500 mr-2">✓</span>{' '}
                  Custom integrations
                </li>
                <li className="flex items-center text-gray-300">
                  <span className="text-green-500 mr-2">✓</span>{' '}
                  SLA guarantee
                </li>
              </ul>
              <button className="w-full py-3 border border-purple-500 text-purple-400 rounded-lg hover:bg-purple-500/10 transition">
                Contact Sales
              </button>
            </div>
          </div>
        </div>

        {/* Use Cases */}
        <div className="bg-black/30 py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-4xl font-bold text-white text-center mb-12">Built For</h2>
            
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-6xl mb-4">💬</div>
                <h3 className="text-xl font-bold text-white mb-3">Discord Servers</h3>
                <p className="text-gray-400">Auto-moderate uploaded media and protect your community from deepfake scams</p>
              </div>

              <div className="text-center">
                <div className="text-6xl mb-4">✈️</div>
                <h3 className="text-xl font-bold text-white mb-3">Telegram Groups</h3>
                <p className="text-gray-400">Detect manipulated photos and videos before they spread misinformation</p>
              </div>

              <div className="text-center">
                <div className="text-6xl mb-4">🖼️</div>
                <h3 className="text-xl font-bold text-white mb-3">NFT Marketplaces</h3>
                <p className="text-gray-400">Verify authenticity of profile pictures and digital art to prevent fraud</p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to protect your community?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Start with 10 free scans. No credit card required.
          </p>
          <button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} className="inline-block px-10 py-5 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-lg font-semibold rounded-lg hover:from-purple-700 hover:to-pink-700 transition">
            Get Your API Key Now →
          </button>
        </div>

        {/* Footer */}
        <footer className="bg-black/50 border-t border-purple-500/30 py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <div className="flex items-center space-x-2 mb-4 md:mb-0">
                <span className="text-2xl">🛡️</span>
                <span className="text-xl font-bold text-white">DeepfakeGuard</span>
              </div>
              <div className="flex space-x-6 text-gray-400 text-sm">
                <button className="hover:text-white transition">Privacy Policy</button>
                <button className="hover:text-white transition">Terms of Service</button>
                <button className="hover:text-white transition">API Status</button>
                <button className="hover:text-white transition">Contact</button>
              </div>
            </div>
            <p className="text-center text-gray-500 text-sm mt-4">
              © 2025 DeepfakeGuard. All rights reserved.
            </p>
          </div>
        </footer>
      </div>

      <style global jsx>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
        
        * {
          font-family: 'Inter', sans-serif;
        }
      `}</style>
    </>
  );
}
