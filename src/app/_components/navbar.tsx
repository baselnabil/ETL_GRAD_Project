"use client"
import React, { useEffect } from 'react';
import { themeChange } from 'theme-change';
import Link from 'next/link';


const ThemeSelect: React.FC = () => {
    useEffect(() => {
        themeChange(false);
    }, []);    
    return (
            <select className="select select-bordered w-min md:w-auto bg-base-200 bg-opacity-60 backdrop-blur-md" data-choose-theme>
                <option disabled value="">Pick a theme</option>
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="sunset">sunset</option>
                <option value="cmyk">cmyk</option>
            </select>
    );
};

interface NavbarProps {
  docTitle?: string;
}

const truncateTitle = (title: string, maxLength: number) => {
  if (title.length <= maxLength) return title;
  return title.slice(0, maxLength) + '...';
};

const Navbar: React.FC<NavbarProps> = ({ docTitle }) => {
  const truncatedTitle = docTitle ? truncateTitle(`GS - ${docTitle}`, 26) : "GradSync";

  return (
    <nav className="navbar bg-base-200 bg-opacity-60 backdrop-blur-md border-b border-opacity-20 border-transparent">
      <div className="w-full flex justify-between md:hidden">
        <Link className="btn btn-ghost text-lg font-bold truncate sm:max-w-full overflow-hidden"  href="/">
          {truncatedTitle}
        </Link>

        <div className="dropdown dropdown-end">
          <button className="btn btn-ghost">
            <i className="fa-solid fa-bars text-sm">Menu</i>
          </button>

          <ul tabIndex={0} className="dropdown-content menu z-[1] bg-base-200 bg-opacity-60 backdrop-blur-md p-6 rounded-box shadow w-56 gap-2">
            <li><Link href="/docs/getting-started/overview">Docs</Link></li>
            <Link href="/team" className="btn btn-ghost">The Team</Link>
            <li><Link href="https://github.com/baselnabil/ETL_GRAD_Project" target="_blank">Repo</Link></li>
            <li className="divider"></li>
            <li className="flex justify-center items-center"> <ThemeSelect /> </li>
          </ul>
        </div>
      </div>

      <div className="w-full hidden md:flex justify-between items-center">
        <div className="flex space-x-4">
          <Link href="/docs/getting-started/overview" className="btn btn-ghost">Docs</Link>
          <Link href="/team" className="btn btn-ghost">The Team</Link>
          <Link href="https://github.com/baselnabil/ETL_GRAD_Project" target="_blank" className="btn btn-ghost">Repo</Link>
        </div>

        <Link className="btn btn-ghost text-lg" href="/">
        {docTitle ? `GradSync - ${docTitle}` : "GradSync"}
        </Link>

        <div>
        <ThemeSelect />
    </div>
      </div>
    </nav>
  );
};

export default Navbar;