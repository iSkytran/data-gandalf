"use client";
import { useState, useEffect } from "react";
import Grid from "../../components/grid";

export default function Dataset({ params }: { params: { dataset: string } }) {
  const [datasets, setDatasets] = useState([]);
  const [ratings, setRatings] = useState([]);

  useEffect(() => {
    const datasetUrl = `/api/datasets/${encodeURIComponent(params.dataset)}`;
    fetch(datasetUrl)
      .then((res) => res.json())
      .then((data) => {
        setDatasets(data);
      });
  }, [params.dataset]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Grid datasets={datasets} ratings={ratings}/>
    </main>
  );
}
