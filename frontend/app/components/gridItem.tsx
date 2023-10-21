import Link from "next/link";
import Rating from "./rating";

export default function GridItem({ metadata, rating }: { metadata: any, rating: any }) {
  return (
    <Link href={`/dataset/${metadata.id}`}>
      <div className="w-64 shadow-lg rounded-lg p-6 border overflow-hidden bg-white">
        <h2 className="text-xl font-bold">{metadata.name}</h2>
        <p className="font-semibold my-1">{metadata.topic}</p>
        <p className="text-sm">{metadata.description}</p>
        <p className="text-sm">{metadata.license}</p>
        <p className="text-sm">{metadata.tags}</p>
          {rating ? (
            <Rating rating={rating}/>
            ) : null
          }
      </div>
    </Link>
  );
}
