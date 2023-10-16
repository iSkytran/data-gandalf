import GridItem from "./gridItem";

export default function Grid({ datasets }: { datasets: Array<object> }) {
  if (!datasets) {
    return <div>Loading...</div>;
  }

  console.log(datasets);

  const items = datasets.map((dataset: any) => {
    return <GridItem key={dataset.id} metadata={dataset} />;
  });
  return <div className="grid grid-cols-4 gap-4">{items}</div>;
}
