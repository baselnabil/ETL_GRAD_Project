import fs from "node:fs";
import path from "node:path";
import { useMDXComponents } from "@/mdx-components";
import { compileMDX } from "next-mdx-remote/rsc";
import rehypeHighlight from "rehype-highlight";
import rehypeSlug from "rehype-slug";
import remarkGfm from "remark-gfm";
import Navbar from "@/app/_components/navbar";
import { DocsMenu } from "../Nav";

export const runtime = "nodejs";
export const dynamic = "force-static";

const contentSource = "src/app/docs/content";


interface Params {
	params: {
		slug: string[];
	};
}

export default async function DocsPage({ params }: Params) {
	// Read the MDX file from the content source direectory
    const filePath = path.join(process.cwd(), contentSource, params.slug.join("/")) + ".mdx";

    // Check if the file exists, if not, use the 404 file
    const source = fs.existsSync(filePath)
        ? fs.readFileSync(filePath, "utf8")
        : fs.readFileSync(path.join(process.cwd(), contentSource, "404.mdx"), "utf8");


	// MDX accepts a list of React components
	const components = useMDXComponents({});

	// We compile the MDX content with the frontmatter, components, and plugins
	const { content, frontmatter } = await compileMDX({
		source,
		options: {
			mdxOptions: {
				rehypePlugins: [rehypeHighlight, rehypeSlug],
				remarkPlugins: [remarkGfm],
			},
			parseFrontmatter: true,
		},
		components,
	});

	// (Optional) Set some easy variables to assign types, because TypeScript
	const pageTitle = frontmatter.title as string;
	const pageDescription = frontmatter.description as string;

    return (
        <>
        <Navbar docTitle={pageTitle} />
        <div className="flex flex-col lg:flex-row h-screen">
          <aside className="w-full lg:w-1/6 p-4 bg-base-200 h-full overflow-y-auto">
            <DocsMenu />
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
