import mdx from '@next/mdx';
import rehypeSlug from "rehype-slug";
import remarkGfm from "remark-gfm";
import rehypeImageSize from "./src/lib/rehype-image-size.mjs"

const withMDX = mdx({
  extension: /\.mdx?$/,
    options: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [rehypeSlug, [rehypeImageSize, { root: process.cwd() }]],
  }
});
 
/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'export',
    images: {
      unoptimized: true,
    },
    basePath: process.env.NODE_ENV === "development" ? "":`/${process.env.REPO_NAME}`,
  // Configure `pageExtensions` to include MDX files
  pageExtensions: ['js', 'jsx', 'mdx', 'ts', 'tsx'],
  // Optionally, add any other Next.js config below
}
 
export default withMDX(nextConfig);

