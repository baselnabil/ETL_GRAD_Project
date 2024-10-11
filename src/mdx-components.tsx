import type { MDXComponents } from "mdx/types";
import Image, { ImageProps } from "next/image";
import Link from "next/link";
import React from "react";

// Define custom MDX components
export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
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
    img: (props) => (
      <Image className="rounded-lg shadow-lg" alt={props.alt || ""} {...(props as Omit<ImageProps, 'alt'>)} />
    ),
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
    code: ({ children }) => (
      <code className="bg-base-200 rounded p-1">{children}</code>
    ),
    pre: ({ children }) => (
      <pre className="bg-base-200 rounded p-4 overflow-auto my-4">
        {children}
      </pre>
    ),
    // Spread the passed components to allow overriding
    ...components,
  };
}