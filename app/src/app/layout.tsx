import { Roboto_Slab } from "next/font/google";
import { SessionProvider } from "next-auth/react";
import "./globals.css";
import Navbar from "./components/navbar/navBar";

const inter = Roboto_Slab({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
 
  return (
    <html lang="en">
      <body className={inter.className}>
        <SessionProvider>
          <Navbar />
          <div style={{ flex: '1 0 auto' }}>
            {children}
          </div>
        </SessionProvider>
      </body>
    </html>
  );
}
