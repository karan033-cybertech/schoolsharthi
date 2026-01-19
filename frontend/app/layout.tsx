import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  metadataBase: new URL('https://schoolsharthi.com'),
  title: {
    default: 'SchoolSharthi - Indian Education Platform',
    template: '%s | SchoolSharthi'
  },
  description: 'Premium handwritten notes, PYQs, AI-powered doubt solver, and career guidance for Class 6-12 students. Har Student Ka Sacha Sarthi.',
  keywords: ['education', 'notes', 'PYQs', 'AI doubt solver', 'career guidance', 'Class 6-12', 'Indian education'],
  authors: [{ name: 'SchoolSharthi' }],
  creator: 'SchoolSharthi',
  publisher: 'SchoolSharthi',
  robots: {
    index: true,
    follow: true,
  },
  openGraph: {
    type: 'website',
    locale: 'en_IN',
    url: 'https://schoolsharthi.com',
    siteName: 'SchoolSharthi',
    title: 'SchoolSharthi - Indian Education Platform',
    description: 'Premium handwritten notes, PYQs, AI-powered doubt solver, and career guidance for Class 6-12 students.',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'SchoolSharthi - Indian Education Platform',
    description: 'Premium handwritten notes, PYQs, AI-powered doubt solver, and career guidance for Class 6-12 students.',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
