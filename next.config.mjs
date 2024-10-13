import mdx from '@next/mdx';
import rehypeSlug from "rehype-slug";
import remarkGfm from "remark-gfm";


const withMDX = mdx({
  extension: /\.mdx?$/,
  options: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [rehypeSlug],
  },
});
 
/** @type {import('next').NextConfig} */
const nextConfig = {
    basePath: process.env.NODE_ENV === "development" ? "":"/ETL_GRAD_Project",
    output: "export",
  // Configure `pageExtensions` to include MDX files
  pageExtensions: ['js', 'jsx', 'mdx', 'ts', 'tsx'],
  // Optionally, add any other Next.js config below
}
 
export default withMDX(nextConfig);

