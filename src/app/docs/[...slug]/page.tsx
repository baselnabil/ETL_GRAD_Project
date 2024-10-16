import fs from "node:fs";
import path from "node:path";
import components from "@/mdx-components";
import { compileMDX } from "next-mdx-remote/rsc";
import rehypeSlug from "rehype-slug";
import remarkGfm from "remark-gfm";
import Navbar from "@/app/_components/navbar";
import { DocsMenu } from "../Nav";
import React from "react";


const contentSource = "src/app/docs/content";


interface Params {
	params: {
		slug: string[];
	};
}

interface Heading {
  id: number;
  slug: string;
  title: string;
  level: number;
}

interface ExtractHeadingsOptions {
  slugFn?: (title: string) => string;
}

export function extractHeadings(
  content: string,
  options?: ExtractHeadingsOptions
): Array<Heading> {
  const headings: Array<Heading> = [];
  const headingMatcher = /^(#+)\s(.+)$/gm;

  let match = headingMatcher.exec(content);
  while (match !== null) {
    const id = Math.floor(Math.random() * 900000) + 100000;
    const level = match[1].length;
    const title = match[2].trim();
    const slugFn = options?.slugFn ?? defaultSlugFn;
    const slug = slugFn(title);

    headings.push({ id, slug, title, level });
    match = headingMatcher.exec(content);
  }

  return headings;
}

const defaultSlugFn = (title: string): string => {
  return title
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-");
};

export default async function DocsPage({ params }: Params) {
	// Read the MDX file from the content source direectory
    const filePath = path.join(process.cwd(), contentSource, params.slug.join("/")) + ".mdx";

    // Check if the file exists, if not, use the 404 file
    const source = fs.existsSync(filePath)
        ? fs.readFileSync(filePath, "utf8")
        : fs.readFileSync(path.join(process.cwd(), contentSource, "404.mdx"), "utf8");


	// We compile the MDX content with the frontmatter, components, and plugins
	const { content, frontmatter } = await compileMDX({
		source,
		options: {
			mdxOptions: {
				rehypePlugins: [ rehypeSlug],
				remarkPlugins: [remarkGfm],
			},
			parseFrontmatter: true,
		},
		components,
	});

	// (Optional) Set some easy variables to assign types, because TypeScript
	const pageTitle = frontmatter.title as string;
	const pageDescription = frontmatter.description as string;

  // Extract headings from the content
  const headings = extractHeadings(source);

    return (
        <>
        <Navbar docTitle={pageTitle} />
        <div className="flex flex-col lg:flex-row h-screen">
        <aside className="w-full lg:w-1/6 p-4 bg-base-200 h-full overflow-y-auto transition-all duration-300">
          <DocsMenu headings={headings} />
        </aside>
          <main className="w-full lg:w-5/6 p-4 overflow-y-auto">
            <h1 className="text-4xl font-bold mb-4">{pageTitle}</h1>
            <p className="text-lg text-gray-600 mb-4">{pageDescription}</p>
            <div className="prose max-w-none">{content}</div>
          </main>
        </div>
      </>
      );
    }




export function generateStaticParams() {
  // Recursively fetech all files in the content directory
	const targets = fs.readdirSync(path.join(process.cwd(), contentSource), {
		recursive: true,
	});

  // Declare an empty array to store the files
	const files = [];

	for (const target of targets) {
    // If the target is a directory, skip it, otherwise add it to the files array
		if (
			fs
				.lstatSync(
					path.join(process.cwd(), contentSource, target.toString()),
				)
				.isDirectory()
		) {
			continue;
		}

    // Built the files array
		files.push(target);
	}

  // Return the files array with the slug (filename without extension)
	return files.map((file) => ({
		slug: file.toString().replace(".mdx", "").split("/"),
	}));
}
