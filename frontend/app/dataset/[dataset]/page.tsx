"use client";
import { useState, useEffect } from "react";
import Grid from "../../components/grid";
import GridItem from "../../components/gridItem";
import Rating from "../../components/rating";

export default function Dataset({ params }: { params: { dataset: string } }) {
  const [datasets, setDatasets] = useState([]);

  useEffect(() => {
    const datasetUrl = `/api/datasets/${encodeURIComponent(params.dataset)}`;
    fetch(datasetUrl)
      .then((res) => res.json())
      .then((data) => {
        setDatasets(data);
      });
  }, [params.dataset]);

  const items = datasets.map((dataset: any) => {
    return (
      <GridItem key={dataset.id} metadata={dataset}>
      </GridItem>
    );
  });

  if (!datasets) {
    return <div>Loading...</div>;
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Grid>
        {items}
      </Grid>
    </main>
  );
}
