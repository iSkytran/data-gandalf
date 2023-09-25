import { useState, useEffect } from 'react';
import GridItem from "./gridItem";

export default function Grid({ selectedTopic }: { selectedTopic: string }) {
  const [datasets, setDatasets] = useState([]);

  useEffect(() => {
    let url = `/api/datasets?topic=${encodeURIComponent(selectedTopic)}`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setDatasets(data);
      });
  }, [selectedTopic]);

  if (!datasets) {
    return (
      <div>Loading...</div>
    );
  }


  let items = datasets.map((dataset: any) => {
    return <GridItem key={dataset.id} metadata={dataset} />
  }
  );
  return (
    <div className="grid grid-cols-4 gap-4">
      {items}
    </div>
  );
}
