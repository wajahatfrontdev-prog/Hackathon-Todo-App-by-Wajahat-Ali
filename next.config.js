/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['framer-motion', 'lucide-react'],
    turbo: {
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production'
  },
  images: {
    unoptimized: false,
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 31536000
  },
  swcMinify: true,
  poweredByHeader: false,
  compress: true
}

module.exports = nextConfig