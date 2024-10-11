import Link from "next/link";
import { ReactNode } from "react";
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
      { href: "/docs/data/etl-loading", label: "ETL - Loading" },
      { href: "/docs/data/ab2", label: "ab2" },
      { href: "/docs/data/settings", label: "Settings" },
    ],
  },
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

export const DocsMenu = () => {
  return (
    <div className="p-4">
      {DocsNav.map((menuItem) => (
        <div key={menuItem.header} className="mb-4">
          <NavHeader
            title={menuItem.header}
            color={menuItem.color}
          >
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
    </div>
  );
};