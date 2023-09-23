import GridItem from "./gridItem";

async function getAllDatasets() {
  const res = await fetch('http://localhost:8080/datasets')
  if (!res.ok) {
    throw new Error('Failed to get datasets.');
  }
  return res.json();
}

export default async function Grid() {
  const datasets = await getAllDatasets();
  let items = datasets.map((dataset: any) => {
      return <GridItem key={dataset.id} name={dataset.name} />
    }
  );
  return (
    <>
      <ul>{items}</ul>
    </>
  );
}
