"use client";
import { useState, useEffect } from "react";
import FilterBar from "./components/filterBar";
import Grid from "./components/grid";

export default function Home() {
  const [datasets, setDatasets] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("");

  useEffect(() => {
    let url = `/api/datasets?topic=${encodeURIComponent(selectedTopic)}`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setDatasets(data);
        console.log(data);
      });
  }, [selectedTopic]);

  return (
    <>
      <header className="flex p-6 fixed top-0 w-full bg-white shadow-md">
        <h1 className="flex-auto basis-4/6 text-4xl font-bold text-sas_blue">
          Data Gandalf
        </h1>
        <FilterBar
          className="flex-auto basis-2/6"
          setSelectedTopic={setSelectedTopic}
        />
      </header>
      <main className="flex min-h-screen flex-col items-center justify-between p-24 bg-zinc-100">
        <h2 className="text-3xl font-semibold text-center m-6 text-sas_blue">
          Find relevant datasets by filtering with a topic or through selecting
          a dataset.
        </h2>
        <Grid datasets={datasets} />
      </main>
    </>
  );
}
