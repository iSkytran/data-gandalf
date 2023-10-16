"use client";
import { useState, useEffect } from "react";
import Grid from "../../components/grid";

export default function Dataset({ params }: { params: { dataset: string } }) {
  const [datasets, setDatasets] = useState([]);

  useEffect(() => {
    const url = `/api/dataset/${encodeURIComponent(params.dataset)}`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        let data_with_similarity = data.map((data) => {
          let similarity = data[0];
          let dataset = data[1][0];
          dataset.similarity = similarity;
          return dataset;
        })
        setDatasets(data_with_similarity);
      });
  }, [params.dataset]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Grid datasets={datasets} />
    </main>
  );
}
