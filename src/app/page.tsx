import Navbar from "@/app/_components/navbar";
import Link from 'next/link';

export default function Home() {
  return (
    <>
      <Navbar />
      <div className="hero bg-base-200 min-h-screen">
        <div className="text-center flex flex-col items-center gap-6 max-w-lg p-6">

          <h1 className="font-bold text-5xl  whitespace-nowrap">
            GradSync <span className="text-primary">Documentation</span>
          </h1>

          <span className="text-lg">
            Welcome to the official documentation site for our GradSync! The Final Graduation Project for The DEPI Initiative, Data Engineering track
          </span>

          <div className="flex flex-col sm:flex-row gap-4">
            <Link className="btn btn-primary" href="/docs/getting-started/overview">
              <i className="fa-solid fa-book mr-2"></i>
              Read the Docs
            </Link>

            <Link className="btn btn-secondary" href="https://github.com/baselnabil/ETL_GRAD_Project" target="_blank">
              <i className="fa-solid fa-code-branch mr-2"></i>
              View the Repo
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}