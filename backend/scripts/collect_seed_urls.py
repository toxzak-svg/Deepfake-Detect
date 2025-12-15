"""Small script to collect a seed list of example URLs for labeling.

Usage:
  python collect_seed_urls.py > seed_urls.txt
"""
import sys

SEED = [
    "https://example.com/legit-project-announcement",
    "https://scam.example.com/crypto-airdrop-giveaway",
    "https://youtube.com/watch?v=FAKE_GIVEAWAY",
    "https://t.me/somechannel/12345",
]

def main():
    for u in SEED:
        print(u)

if __name__ == '__main__':
    main()
