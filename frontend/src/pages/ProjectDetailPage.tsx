import { useParams } from "react-router-dom";

export function ProjectDetailPage() {
  const { id } = useParams();

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl font-bold">Project Detail</h1>
      <p>Project ID: {id}</p>
    </div>
  );
}
