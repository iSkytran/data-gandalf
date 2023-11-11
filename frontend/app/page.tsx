"use client";
import { useState, useEffect } from "react";
import FilterBar from "@/app/components/filterBar";
import Grid from "@/app/components/grid";
import GridItem from "@/app/components/gridItem";
import LoadingIcon from "@/app/components/loadingIcon";
import { processMetadata } from "@/app/utilities";

export default function Home() {
  const [datasets, setDatasets] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("");
  const [offset, setOffset] = useState(0);
  const [pageCount, setPageCount] = useState(0);

  useEffect(() => {
    let url =
      "/api/datasets?" +
      new URLSearchParams([
        ["offset", offset.toString()],
        ["topic", selectedTopic],
      ]);

    fetch(url)
      .then((res) => {
        let xCount = res.headers.get("x-total-count");
        let xOffset = res.headers.get("x-offset-count");
        if (xCount) {
          setPageCount(Math.ceil(parseInt(xCount) / 100));
        }
        if (xOffset) {
          setOffset(parseInt(xOffset));
        }
        return res.json();
      })
      .then((data) => {
        data.map((dataset: any) => {
          return processMetadata(dataset);
        });
        setDatasets(data);
      });
  }, [selectedTopic, offset]);

  const pageChange = (event: any) => {
    const newOffset = event.selected * 100;
    setOffset(newOffset);
  };

  const items = datasets.map((dataset: any) => {
    return <GridItem key={dataset.id} metadata={dataset} />;
  });

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
      {datasets && datasets.length > 0 ? (
        <main className="flex flex-col items-center justify-between min-h-screen p-24 bg-zinc-100">
          <h2 className="text-3xl font-semibold text-center mt-6 text-sas_blue">
            Find relevant datasets by filtering with a topic or through
            selecting a dataset.
          </h2>
          <Grid pageCount={pageCount} pageChange={pageChange}>
            {items}
          </Grid>
        </main>
      ) : (
        <main className="flex flex-col items-center justify-center min-h-screen p-24 bg-zinc-100">
          <LoadingIcon />
        </main>
      )}
    </>
  );
}
