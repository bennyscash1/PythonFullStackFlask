import Link from "next/link";
import styles from "./navBar.module.css";
import { usePathname } from 'next/navigation'

import { STRINGS } from "@/app/constants";
import { useCallback } from "react";

const Navbar = () => {
  const pathname = usePathname()

  const navBarPages = Object.values(STRINGS.PAGES); 
  const addActiveClass = useCallback(((path: string) => {
    return (
      `${styles.link} ${pathname === path ? styles.active : ''}`
    )
  }), [pathname]);

  return (
    <nav className={styles.navbar}>
      {navBarPages.map(({NAME, PATH}) => (
        <Link key={PATH} className={addActiveClass(PATH)} href={PATH}>{NAME}</Link>
        ))}
    </nav>
  );
  };

  export default Navbar;