import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import { ThemeSync } from "@/components/ThemeSync";
import "./globals.css";

const font = Montserrat({ subsets: ["latin"], weight: ["300", "400", "500", "600", "700"], variable: "--font" });

export const metadata: Metadata = {
  title: "EVE",
  description: "Gérer. Développer. Réussir.",
};

// Lu avant l’affichage pour éviter un flash. Les valeurs sont re-validées ici.
const themeScript = `(function(){try{var t=JSON.parse(localStorage.getItem("eve.theme.v1")||"{}");var d=document.documentElement;var m=t.mode;var l=m==="light"||(m!=="dark"&&matchMedia("(prefers-color-scheme: light)").matches);d.dataset.theme=l?"light":"dark";if(/^#[0-9a-fA-F]{6}$/.test(t.accent||""))d.style.setProperty("--accent",t.accent);if(typeof t.blur==="number")d.style.setProperty("--glass-blur",Math.min(40,Math.max(8,t.blur))+"px");d.dataset.motion=t.animations===false?"off":"on"}catch(e){}})();`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" className={font.variable} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body>
        <div className="bgfx" aria-hidden="true">
          <i className="o a" />
          <i className="o b" />
          <i className="o c" />
        </div>
        <ThemeSync />
        {children}
      </body>
    </html>
  );
}