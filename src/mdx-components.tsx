import type { MDXComponents } from "mdx/types";
import Image from "next/image";
import Link from "next/link";
import React from "react";
import { PrismLight as SyntaxHighlighter } from "react-syntax-highlighter";
import pythonLang from "react-syntax-highlighter/dist/cjs/languages/prism/python";
import sqlLang from "react-syntax-highlighter/dist/cjs/languages/prism/sql";
import psqlLang from "react-syntax-highlighter/dist/cjs/languages/prism/sql";
import mariadbLang from "react-syntax-highlighter/dist/cjs/languages/prism/sql";
import { oneDark } from "react-syntax-highlighter/dist/cjs/styles/prism";
import CodeBlock from "./app/_components/CodeBlock";


SyntaxHighlighter.registerLanguage("py", pythonLang);

SyntaxHighlighter.registerLanguage("sql", sqlLang);
SyntaxHighlighter.registerLanguage("psql", psqlLang);
SyntaxHighlighter.registerLanguage("mariadb", mariadbLang);

// Define custom MDX components
const components: MDXComponents = {
  a: ({ children, href }: React.DetailedHTMLProps<React.AnchorHTMLAttributes<HTMLAnchorElement>, HTMLAnchorElement>) => (
    <Link href={href ?? "#"} className="link link-primary">
      {children}
    </Link>
  ),
  hr: (props) => (
    <div className="divider my-4" {...props}>
      {props.children}
    </div>
  ),
  Image: (props) => ( <Image {...props} alt={props.alt} /> ),
  h1: ({ children }) => (
    <h1 className="text-4xl font-bold my-4">{children}</h1>
  ),
  h2: ({ children }) => (
    <h2 className="text-3xl font-semibold my-4">{children}</h2>
  ),
  h3: ({ children }) => (
    <h3 className="text-xl font-semibold my-4">{children}</h3>
  ),
  p: ({ children }) => (
    <p className="text-base my-2">{children}</p>
  ),
  ul: ({ children }) => (
    <ul className="list-disc list-inside my-2">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal list-inside my-2">{children}</ol>
  ),
  li: ({ children }) => (
    <li className="my-1">{children}</li>
  ),
  blockquote: ({ children }) => (
    <blockquote className="border-l-4 border-primary pl-4 my-4">
      {children}
    </blockquote>
  ),
  code: ({ className, ...props }) => {
    const hasLang = /language-(\w+)/.exec(className || "");
    return hasLang ? (
      <SyntaxHighlighter
        style={oneDark}
        language={hasLang[1]}
        PreTag="div"
        className="mockup-code scrollbar-thin scrollbar-track-base-content/5 scrollbar-thumb-base-content/40 scrollbar-track-rounded-md scrollbar-thumb-rounded"
        showLineNumbers={true}
        useInlineStyles={true}
      >
        {String(props.children).replace(/\n$/, "")}
      </SyntaxHighlighter>
    ) : (
      <code className={className} {...props} />
    );
  },
  pre: (preProps) => (
    <CodeBlock {...preProps}>{preProps.children}</CodeBlock>
  ),

};

// Export the components
export default components;