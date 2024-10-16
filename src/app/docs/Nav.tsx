"use client";
import Link from "next/link";
import { ReactNode, useState } from "react";
import { Heading } from "@/app/_lib/loadContent";

export const DocsNav = [
  {
    header: "Getting Started",
    color: "purple",
    items: [
      { href: "/docs/getting-started/overview", label: "Overview" },
      { href: "/docs/getting-started/new", label: "Running the project" },
      {
        href: "/docs/getting-started/architecture",
        label: "Project Architecture",
      },
    ],
  },
  {
    header: "Data",
    color: "blue",
    items: [
      { href: "/docs/data/sources", label: "sources" },
      { href: "/docs/data/etl-extraction", label: "ETL - Extraction" },
      { href: "/docs/data/etl-transformation", label: "ETL - Transformation" },
      { href: "/docs/data/psqlstag-setup", label: "PostgreSQL Staging Setup" },
      { href: "/docs/data/maraiaolap-setup", label: "MariaDB OLAP Setup" },
      { href: "/docs/data/etl-loading", label: "ETL - Loading" },
    ],
  },
  {
    header: "Machine Learning",
    color: "purple",
    items: [
      { href: "/docs/ml/ml-overview", label: "ML Overview" },
      { href: "/docs/ml/ml-cexplanation", label: "ML Code Explanation" },
    ]
  },
  {
    header: "Airflow",
    color: "red",
    items: [
      { href: "/docs/airflow/airflow-overview", label: "Airflow Overview" },
      { href: "/docs/airflow/airflow-cexplanation", label: "Airflow Code Explanation" },
    ]
  }
  // ...
];

interface NavHeaderProps {
  title: string;
  color: string;
  children: ReactNode;
}

const NavHeader: React.FC<NavHeaderProps> = ({ title, color, children }) => (
  <div className={`text-${color}-600`}>
    <div className="flex items-center gap-2">
      <h2 className="text-xl font-bold">{title}</h2>
    </div>
    <div className="ml-4">{children}</div>
  </div>
);

interface NavItemProps {
  href: string;
  children: ReactNode;
}

const NavItem: React.FC<NavItemProps> = ({ href, children }) => (
  <Link href={href} className="link no-underline block py-2 px-4 rounded hover:bg-base-300 ">
    {children}
  </Link>
);

interface DocsMenuProps {
  headings: Heading[];
}

export const DocsMenu: React.FC<DocsMenuProps> = ({ headings }) => {
  const [isCollapsed, setIsCollapsed] = useState(true);

  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className={`p-4 ${isCollapsed ? "w-16" : "w-64"} md:w-full transition-all duration-300`}>
      <button
        className="btn btn-ghost md:hidden"
        onClick={toggleCollapse}
      >
        {isCollapsed ? "Show Doc Navigation" : "Hide Doc Navigation"}
      </button>
      <div className={`md:block ${isCollapsed ? "hidden" : "block"}`}>
        {DocsNav.map((menuItem) => (
          <div key={menuItem.header} className="mb-4">
            <NavHeader title={menuItem.header} color={menuItem.color}>
              <div className="flex flex-col gap-1">
                {menuItem.items.map((item) => (
                  <NavItem href={item.href} key={item.label}>
                    {item.label}
                  </NavItem>
                ))}
              </div>
            </NavHeader>
          </div>
        ))}
        <div className="divider"></div>
        <div className="mt-4">
          <h3 className="text-lg font-bold">Table of Contents</h3>
          <ul>
            {headings.map((heading) => (
              <li key={heading.id} className={`ml-${heading.level + 1} mt-2`}>
                <a href={`#${heading.slug}`}>{heading.title}</a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};