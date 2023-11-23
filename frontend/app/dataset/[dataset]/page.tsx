"use client";
import { useState, useEffect } from "react";
import { useCookies } from "react-cookie";
import { v4 as uuidv4 } from "uuid";
import Grid from "@/app/components/grid";
import GridItem from "@/app/components/gridItem";
import GridItemLarge from "@/app/components/gridItemLarge";
import Rating from "@/app/components/rating";
import Link from "next/link";
import LoadingIcon from "@/app/components/loadingIcon";
import { processMetadata } from "@/app/utilities";

export default function Dataset({ params }: { params: { dataset: string } }) {
  const [metadata, setMetadata] = useState<any>(null);
  const [datasets, setDatasets] = useState<any[]>([]);
  const [ratings, setRatings] = useState<any[]>([]);
  const [cookies, setCookie] = useCookies<any>(["user_session"]);

  if (!("user_session" in cookies)) {
    setCookie("user_session", uuidv4());
  }

  useEffect(() => {
    const datasetUrl = `/api/datasets/${encodeURIComponent(params.dataset)}`;
    const ratingUrl = `/api/ratings/?user_session=${encodeURIComponent(
      cookies["user_session"]
    )}&source_dataset=${encodeURIComponent(params.dataset)}`;

    Promise.all([fetch(datasetUrl), fetch(ratingUrl)])
      .then(async (res) => {
        const datasetRes = await res[0].json();
        const ratingRes = await res[1].json();
        return [datasetRes, ratingRes];
      })
      .then((data) => {
        let newMetadata = processMetadata(data[0][0][0]);
        let newDatasets = data[0][1].map((e: any) => {
          const dataset = processMetadata(e[1][0]);
          dataset.similarity = e[0];

          return dataset;
        });
        let newRatings = data[1];

        // Add blank rating element if one was not fetched.
        newDatasets.forEach((newDataset: any) => {
          let ratingIdx: number = newRatings.findIndex(
            (e: any) => e.destination_dataset === newDataset.id
          );
          if (ratingIdx === -1) {
            newRatings.push({
              user_session: cookies["user_session"],
              source_dataset: parseInt(params.dataset),
              destination_dataset: parseInt(newDataset.id),
            });
          }
        });
        setMetadata(newMetadata);
        setDatasets(newDatasets);
        setRatings(newRatings);
      });
  }, [params.dataset, cookies]);

  const items = datasets.map((dataset: any) => {
    const ratingIdx: number = ratings.findIndex(
      (e: any) => e.destination_dataset === dataset.id
    );
    return (
      <GridItem key={dataset.id} metadata={dataset}>
        <Rating
          ratingIdx={ratingIdx}
          ratings={ratings}
          setRatings={setRatings}
        />
      </GridItem>
    );
  });

  return (
    <>
      <header>
        <Link
          className="flex fixed justify-center items-center top-0 w-full bg-white shadow-md"
          href="/"
        >
          <img
            className="max-h-16 px-4"
            src="/original_logo.svg"
            alt="Data Gandalf Logo"
          />
          <h1 className="flex-auto p-6 basis-1 text-4xl font-bold text-sas_blue">
            Data Gandalf
          </h1>
        </Link>
      </header>
      {datasets && datasets.length > 0 ? (
        <main className="flex flex-col items-center justify-between min-h-screen p-24 bg-zinc-100">
          <h1 className="flex-auto m-6 basis-4/6 text-4xl font-bold text-sas_blue">
            Chosen Dataset
          </h1>
          <GridItemLarge metadata={metadata} />
          <h1 className="flex-auto m-6 basis-4/6 text-4xl font-bold text-sas_blue">
            Recommended Datasets
          </h1>
          <Grid>{items}</Grid>
        </main>
      ) : (
        <main className="flex flex-col items-center justify-center min-h-screen p-24 bg-zinc-100">
          <LoadingIcon />
        </main>
      )}
    </>
  );
}
