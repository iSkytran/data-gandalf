import Link from "next/link";

export default function GridItem({ metadata, children }: { metadata: any, children?: React.ReactNode }) {

  return (
    <Link href={`/dataset/${metadata.id}`} passHref legacyBehavior>
      <div className="w-64 shadow-lg rounded-lg p-6 border overflow-hidden bg-white">
        <h2 className="text-xl font-bold">{metadata.name}</h2>
        <p className="font-semibold my-1">{metadata.topic}</p>
        <p className="text-sm">{metadata.description}</p>
        <p className="text-sm">{metadata.license}</p>
        <p className="text-sm">{metadata.tags}</p>
        { children }
      </div>
    </Link>
  );
}
