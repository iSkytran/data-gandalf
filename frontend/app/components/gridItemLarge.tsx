import Link from "next/link";

export default function GridItemLarge({ metadata }: { metadata: any }) {
  if (!metadata) {
    return <div>Loading...</div>;
  }

  return (
    <Link href={`/dataset/${metadata.id}`}>
      <div className="w-full shadow-lg rounded-lg p-6 border overflow-x-hidden overflow-y-scroll bg-white">
        <h2 className="text-xl font-bold underline">{metadata.title}</h2>
        <div className="flex">
          <p className="text-xl font-bold underline">Topic:</p>
          <p className="text-xl font-bold no-underline">
            &nbsp;
            {" "}
            {metadata.topic?.charAt(0)?.toUpperCase() +
              metadata.topic?.slice(1)}
          </p>
        </div>

        <p className="font-semibold my-1 underline">
          <button
            className="bg-sas_blue hover:bf-midnight_blue text-white font-bold py-2 px-4 rounded"
            onClick={() => {
              window.open("https://" + metadata.url);
            }}
          >
            {" "}
            View Source{" "}
          </button>{" "}
        </p>
        <p className="font-semibold my-1 underline">Description:</p>
        <p className="text-sm"> {metadata.description}</p>

        <p className="font-semibold my-1 underline">Licenses:</p>
        <p className="text-sm"> {metadata.licenses}</p>

        <p className="font-semibold my-1 underline">Tags:</p>

        <p className="text-sm">{metadata.tags}</p>
      </div>
    </Link>
  );
}
