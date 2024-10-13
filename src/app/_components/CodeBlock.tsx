"use client";
import React, { useState } from "react";
import CopyToClipboard from "react-copy-to-clipboard";

interface PreProps {
  children: React.ReactNode;
}

const CodeBlock: React.FC<PreProps> = (preProps) => {

    const child = React.Children.only(preProps.children) as React.ReactElement | null;
    const codeElement = React.Children.toArray(child?.props.children).find(
        (element) => React.isValidElement(element) && element.type === "code"
        ) as React.ReactElement | null;
  
  const codeChunk = React.Children.toArray(codeElement?.props.children)
        .filter((element) => {
          if (React.isValidElement(element) && element.type === "span") {
          return !element.props.className?.includes("line-number");
         }
        return true;
     })
        .map((element) => (React.isValidElement(element) ? element.props.children : element))
        .join("");

  const [copyTip, setCopyTip] = useState("Copy code");

  const language = child?.props.children.props.className.replace(/language-/g, "") as string;
  return (
    <div className="relative overflow-x-hidden">
      <button
        style={{
          right: 0,
        }}
        className="tooltip tooltip-left absolute z-40 mr-2 mt-5"
        data-tip={copyTip}
      >
        <CopyToClipboard
          text={codeChunk}
          onCopy={async () => {
            setCopyTip("Copied");
            await new Promise((resolve) => setTimeout(resolve, 500));
            setCopyTip("Copy code");
          }}
        >
            <p className="text-gray-400 m-2">C</p>
        </CopyToClipboard>
      </button>
      <span
        style={{
          bottom: 0,
          right: 0,
        }}
        className="absolute z-40 mb-5 mr-1 rounded-lg bg-base-content/40 p-1 text-xs uppercase text-base-300 backdrop-blur-sm"
      >
        {language}
      </span>
      <pre {...preProps}></pre>
    </div>
  );
};

export default CodeBlock;