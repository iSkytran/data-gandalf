"use client";
import { useState, useEffect } from "react";
import Grid from "../../components/grid";
import GridItemLarge from "../../components/gridItemLarge";


export default function Dataset({ params }: { params: { dataset: string } }) {
  const [dataset, setDataset] = useState(null);
  const [datasets, setDatasets] = useState([]);

  useEffect(() => {
    const url = `/api/dataset/${encodeURIComponent(params.dataset)}`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        let thisDataset = data[0][0];
        let recommendedDatasets = data[1];
        let data_with_similarity = recommendedDatasets.map((data) => {
          let similarity = data[0];
          let dataset = data[1][0];
          dataset.similarity = similarity;
          return dataset;
        })
        setDataset(thisDataset);
        setDatasets(data_with_similarity);
      });
  }, [params.dataset]);

  return (
    <>
      <header className="flex p-6 fixed top-0 w-full bg-white shadow-md">
        <h1 className="flex-auto basis-4/6 text-4xl font-bold text-sas_blue">
          Data Gandalf
        </h1>
      </header>
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <h1 className="flex-auto basis-4/6 text-4xl font-bold text-sas_blue">
            Chosen Dataset
          </h1>
        <GridItemLarge metadata={dataset} />
        <h1 className="flex-auto basis-4/6 text-4xl font-bold text-sas_blue">
          Recommended Datasets
        </h1>
        <Grid datasets={datasets} />
      </main>
    </>
  );
}
