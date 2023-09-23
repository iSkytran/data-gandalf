export default function GridItem({metadata}: {metadata: any}) {
    return (
        <div className="w-64 shadow-lg rounded-lg p-6 border overflow-hidden">
            <h2 className="text-xl font-bold">{metadata.name}</h2>
            <p className="font-semibold my-1">{metadata.topic}</p>
            <p className="text-sm">{metadata.description}</p>
            <p className="text-sm">{metadata.license}</p>
            <p className="text-sm">{metadata.tags}</p>
        </div>
    );
}
