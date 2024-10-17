import React from "react";
import Navbar from "@/app/_components/navbar";
import AnimatedBackground from "@/app/_components/AnimatedBackground";

const TeamMember: React.FC<{ name: string; position: string }> = ({
  name,
  position,
}) => (
  <div className="card w-full bg-base-100 shadow-xl">
    <div className="card-body">
      <h2 className="card-title">{name}</h2>
      <p>{position}</p>
    </div>
  </div>
);

const TeamOverview: React.FC = () => {
  const teamMembers = [
    { name: "Basil Nabil Mekky", position: "Team leader - [Airflow, Docker, Database]" },
    { name: "Youssef Reda Mohamed", position: "Team member - [ML - Database - Docs Site]" },
    { name: "Nadia Talaat Hassan", position: "Team member - [Airflow - ML - PowerBI]" },
    { name: "Youssof Waleed Fathi", position: "Team member - [Database - Docs]" },
    { name: "Mohamed Ahmed Abdel Fattah", position: "Team member - [Database - Presentation" },
    { name: "Amr Khaled Saber", position: "Team member - [Database - PowerBI" },
  ];


  return (
    <div className="relative min-h-screen bg-base-100">
      <AnimatedBackground />
      <Navbar />
      <div className="container mx-auto p-4 relative z-10">
        <h1 className="text-4xl font-bold text-center mb-8">Our Team</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {teamMembers.map((member) => (
            <TeamMember
              key={member.name}
              name={member.name}
              position={member.position}
            />
          ))}
        </div>
      </div>
    </div>
  );
};


export default TeamOverview;