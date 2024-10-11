import { DocsMenu } from "./Nav";
import Navbar from "@/app/_components/navbar";

export default function DocsLandingPage() {
  return (
    <>
    <Navbar />
    <div className="flex flex-col lg:flex-row">
      <aside className="w-full lg:w-1/4 p-4 bg-base-200">
        <DocsMenu />
      </aside>
      <main className="w-full lg:w-3/4 p-4">
        <h1 className="text-4xl font-bold mb-4">Documentation</h1>
        <p className="text-lg mb-4">
          Welcome to the documentation. You will be redirected to the Getting Started page shortly.
        </p>
      </main>
    </div>
    </>
  );
}