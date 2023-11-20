import Link from "next/link";

export default function GridItem({
  metadata,
  children,
}: {
  metadata: any;
  children?: React.ReactNode;
}) {
  console.log(metadata.similarityStyle);
  return (
    <div className="w-full shadow-lg rounded-lg p-6 border overflow-x-hidden overflow-y-scroll bg-white">
      <Link href={`/dataset/${metadata.id}`}>
        <h2 className="text-xl font-bold underline">{metadata.title}</h2>
      </Link>

      <p
        style={metadata.topicStyle}
        className="flex-initial text-l max-w-fit border-medium_blue bg-blue-100 text-midnight_blue border-2 rounded my-2 px-2.5 py-0.5 font-semibold"
      >
        {metadata.topic}
      </p>

      {children}

      {metadata.similarity && (
        <p className="my-1">
          <span className="font-semibold">Similarity: </span>
          <span className="flex-initial text-l max-w-fit border-medium_blue bg-blue-100 text-midnight_blue border-2 rounded my-2 px-2.5 py-0.5 font-semibold"
          style={metadata.similarityStyle}>{Math.round(100 * metadata.similarity) / 100}</span>
        </p>
      )}

      <p className="my-1">
        <span className="font-semibold">Licenses: </span>
        <span>{metadata.licenses}</span>
      </p>

      <p className="my-1">
        <span className="font-semibold">Tags: </span>
        <span>{metadata.tags}</span>
      </p>
    </div>
  );
}
