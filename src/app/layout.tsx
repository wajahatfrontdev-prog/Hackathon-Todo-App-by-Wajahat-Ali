'use client';

import './globals.css';
import { Navbar } from '@/components/Navbar';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body style={{fontFamily: 'Inter, sans-serif', willChange: 'transform'}}>
        <Navbar />
        <div style={{transform: 'translateZ(0)'}}>
          {children}
        </div>
      </body>
    </html>
  );
}