"use client";
import { useState, useEffect } from "react";
import Grid from "../../components/grid";
import GridItem from "../../components/gridItem";
import Rating from "../../components/rating";
import { useCookies } from "react-cookie";
import { v4 as uuidv4 } from "uuid";

export default function Dataset({ params }: { params: { dataset: string } }) {
  const [datasets, setDatasets] = useState<any[]>([]);
  const [ratings, setRatings] = useState<any[]>([]);
  const [cookies, setCookie] = useCookies<any>(["user_session"]);
  if (!("user_session" in cookies)) {
    setCookie("user_session", uuidv4());
  }

  useEffect(() => {
    const datasetUrl = `/api/datasets/${encodeURIComponent(params.dataset)}`;
    const ratingUrl = `/api/ratings/?user_session=${encodeURIComponent(cookies["user_session"])}&source_dataset=${encodeURIComponent(params.dataset)}`;

    Promise.all([
      fetch(datasetUrl),
      fetch(ratingUrl),
    ]).then(async(res) => {
        const datasetRes = await res[0].json();
        const ratingRes = await res[1].json();
        return [datasetRes, ratingRes];
    }).then((data) => {
        let newDatasets = data[0];
        let newRatings = data[1];

        // Add blank rating element if one was not fetched.
        newDatasets.forEach((dataset: any) => {
          let ratingIdx: number = newRatings.findIndex((e: any) => e.destination_dataset === dataset.id);
          if (ratingIdx === -1) {
            newRatings.push({
              user_session: cookies["user_session"],
              source_dataset: parseInt(params.dataset),
              destination_dataset: parseInt(dataset.id),
            });
          }
        });
        setDatasets(newDatasets);
        setRatings(newRatings);
    });

  }, [params.dataset]);

  if (!(datasets && ratings)) {
    return <div>Loading...</div>;
  }

  const items = datasets.map((dataset: any) => {
    const ratingIdx: number = ratings.findIndex((e: any) => e.destination_dataset === dataset.id);
    return (
      <GridItem key={dataset.id} metadata={dataset}>
        <Rating ratingIdx={ratingIdx} ratings={ratings} setRatings={setRatings} />
      </GridItem>
    );
  });

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Grid>
        {items}
      </Grid>
    </main>
  );
}

