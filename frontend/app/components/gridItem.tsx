import Link from "next/link";

export default function GridItem({ metadata }: { metadata: any }) {
  return (
    <Link href={`/dataset/${metadata.id}`}>
      <div className="w-64 h-80 shadow-lg rounded-lg p-6 border overflow-x-hidden overflow-y-scroll bg-white">
        <h2 className="text-xl font-bold underline">{metadata.title}</h2>
        <p className="font-semibold my-1 ">Topic:</p>
        <p className="text-l"> {metadata.topic}</p>
        <p className="font-semibold my-1 underline">Description:</p>
        <p className="text-sm"> {metadata.description}</p>

        <p className="font-semibold my-1 underline">Licenses:</p>
        <p className="text-sm"> {metadata.licenses?.join(', ')}</p>

        <p className="font-semibold my-1 underline">Tags:</p>

        <p className="text-sm">{metadata.tags?.join(', ')}</p>
      </div>
    </Link>
  );
}
