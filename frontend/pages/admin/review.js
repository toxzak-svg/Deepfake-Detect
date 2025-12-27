import { useState, useEffect } from 'react';
import Head from 'next/head';

export default function AdminReview() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [adminKey, setAdminKey] = useState('');
  const [authenticated, setAuthenticated] = useState(false);

  const fetchPendingReviews = async (key) => {
    try {
      const response = await fetch('/api/admin/pending-reviews', {
        headers: {
          'X-Admin-Key': key,
        },
      });

      if (response.status === 403) {
        setAuthenticated(false);
        alert('Invalid admin key');
        return;
      }

      const data = await response.json();
      setReviews(data.pending_reviews || []);
      setAuthenticated(true);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching reviews:', error);
      setLoading(false);
    }
  };

  const handleLogin = (e) => {
    e.preventDefault();
    fetchPendingReviews(adminKey);
  };

  const submitDecision = async (scanId, verdict, notes) => {
    try {
      const response = await fetch('/api/admin/review-decision', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Admin-Key': adminKey,
        },
        body: JSON.stringify({
          scan_id: scanId,
          verdict,
          notes,
        }),
      });

      if (response.ok) {
        // Remove from list
        setReviews(reviews.filter((r) => r.scan_id !== scanId));
        alert('Review submitted successfully');
      }
    } catch (error) {
      alert('Error submitting review');
    }
  };

  if (!authenticated) {
    return (
      <>
        <Head>
          <title>Admin Login - DeepfakeGuard</title>
        </Head>
        <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
          <div className="bg-gray-800 rounded-lg p-8 max-w-md w-full">
            <h1 className="text-2xl font-bold text-white mb-6">Admin Login</h1>
            <form onSubmit={handleLogin}>
              <input
                type="password"
                value={adminKey}
                onChange={(e) => setAdminKey(e.target.value)}
                placeholder="Admin Key"
                className="w-full px-4 py-3 bg-gray-700 text-white rounded-lg mb-4"
                required
              />
              <button
                type="submit"
                className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition"
              >
                Login
              </button>
            </form>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Head>
        <title>Manual Review Queue - DeepfakeGuard Admin</title>
      </Head>

      <div className="min-h-screen bg-gray-900 text-white">
        <nav className="bg-gray-800 border-b border-gray-700 p-4">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <h1 className="text-2xl font-bold">🛡️ Manual Review Queue</h1>
            <div className="flex items-center space-x-4">
              <span className="bg-purple-600 px-4 py-2 rounded-full text-sm font-semibold">
                {reviews.length} Pending
              </span>
              <button
                onClick={() => fetchPendingReviews(adminKey)}
                className="bg-gray-700 px-4 py-2 rounded-lg hover:bg-gray-600 transition"
              >
                Refresh
              </button>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto p-6">
          {loading ? (
            <div className="text-center py-12">
              <div className="text-xl text-gray-400">Loading reviews...</div>
            </div>
          ) : reviews.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">✅</div>
              <div className="text-2xl text-gray-400">All caught up!</div>
              <p className="text-gray-500 mt-2">No pending reviews</p>
            </div>
          ) : (
            <div className="space-y-6">
              {reviews.map((review) => (
                <ReviewCard
                  key={review.timestamp}
                  review={review}
                  onDecision={submitDecision}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}

function ReviewCard({ review, onDecision }) {
  const [notes, setNotes] = useState('');
  const [showImage, setShowImage] = useState(false);

  const getSeverityColor = (score) => {
    if (score > 0.8) return 'bg-red-500';
    if (score > 0.6) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <span className={`h-3 w-3 rounded-full ${getSeverityColor(review.score)}`}></span>
            <span className="text-sm text-gray-400">
              {new Date(review.timestamp).toLocaleString()}
            </span>
            <span className="text-sm text-gray-500">•</span>
            <span className="text-sm text-gray-400">{review.email}</span>
          </div>

          <div className="mb-3">
            <a
              href={review.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 break-all"
            >
              {review.url}
            </a>
          </div>

          <div className="flex items-center space-x-6 mb-4">
            <div>
              <div className="text-sm text-gray-400">Detection Score</div>
              <div className="text-3xl font-bold">{(review.score * 100).toFixed(1)}%</div>
            </div>
            {review.flags && review.flags.length > 0 && (
              <div>
                <div className="text-sm text-gray-400">Flags</div>
                <div className="flex flex-wrap gap-2 mt-1">
                  {review.flags.map((flag) => (
                    <span
                      key={flag}
                      className="bg-red-900/50 text-red-300 px-3 py-1 rounded-full text-xs"
                    >
                      {flag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <button
            onClick={() => setShowImage(!showImage)}
            className="text-purple-400 hover:text-purple-300 text-sm mb-3"
          >
            {showImage ? '▼ Hide Media' : '▶ Preview Media'}
          </button>

          {showImage && (
            <div className="mb-4">
              <img
                src={review.url}
                alt="Flagged content"
                className="max-w-full max-h-96 rounded-lg border border-gray-600"
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            </div>
          )}

          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add review notes (optional)..."
            className="w-full bg-gray-700 text-white rounded-lg px-4 py-3 mb-4"
            rows={3}
          />
        </div>
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => onDecision(review.timestamp, 'confirmed', notes)}
          className="flex-1 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 rounded-lg transition"
        >
          ✗ Confirm Deepfake
        </button>
        <button
          onClick={() => onDecision(review.timestamp, 'false_positive', notes)}
          className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-lg transition"
        >
          ✓ False Positive
        </button>
        <button
          onClick={() => onDecision(review.timestamp, 'uncertain', notes)}
          className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 rounded-lg transition"
        >
          ? Uncertain
        </button>
      </div>
    </div>
  );
}
