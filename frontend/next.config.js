/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // Enable for Azure Container Apps
  poweredByHeader: false,
}

module.exports = nextConfig
