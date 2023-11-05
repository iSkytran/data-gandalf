import Link from "next/link";

export default function GridItem({ metadata, children }: { metadata: any, children?: React.ReactNode }) {
  return (
    <div className="w-full shadow-lg rounded-lg p-6 border overflow-x-hidden overflow-y-scroll bg-white">
      <Link href={`/dataset/${metadata.id}`}>
        <h2 className="text-xl font-bold underline">{metadata.title}</h2>
        {metadata.similarity && <p className="font-semibold my-1 ">Similarity: {Math.round(10000 * metadata.similarity)/100}</p>}
        <p className="text-l"><span className="font-semibold my-1 ">Topic: </span>{metadata.topic}</p>
        <p className="font-semibold my-1 underline">Licenses:</p>
        <p className="text-sm"> {metadata.licenses?.join(', ')}</p>
        <p className="font-semibold my-1 underline">Tags:</p>
        <p className="text-sm">{metadata.tags?.join(', ')}</p>
      </Link>
      { children }
    </div>
  );
}

