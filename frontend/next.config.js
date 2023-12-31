/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.BACKEND_ADDRESS}/:path*`
      }
    ]
  }
}

module.exports = nextConfig
