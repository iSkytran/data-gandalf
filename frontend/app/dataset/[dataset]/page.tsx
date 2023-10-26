"use client";
import { useState, useEffect } from "react";
import Grid from "../../components/grid";
import GridItem from "../../components/gridItem";
import Rating from "../../components/rating";
import { useCookies } from "react-cookie";
import { v4 as uuidv4 } from "uuid";

export default function Dataset({ params }: { params: { dataset: string } }) {
  const [datasets, setDatasets] = useState([]);
  const [ratings, setRatings] = useState([]);
  const [cookies, setCookie] = useCookies(["user_session"]);
  if (!("user_session" in cookies)) {
    setCookie("user_session", uuidv4());
  }

  useEffect(() => {
    const datasetUrl = `/api/datasets/${encodeURIComponent(params.dataset)}`;
    const ratingUrl = `/api/ratings/?user_session=${encodeURIComponent(cookies["user_session"])}&source_dataset=${encodeURIComponent(params.dataset)}`;
    fetch(datasetUrl)
      .then((res) => res.json())
      .then((data) => {
        setDatasets(data);
      });
    fetch(ratingUrl)
      .then((res) => res.json())
      .then((data) => {
        setRatings(data);
      });
  }, [params.dataset]);

  if (!datasets) {
    return <div>Loading...</div>;
  }

  const items = datasets.map((dataset: any) => {
    let ratingData = ratings.find((e: any) => e.destination_dataset === dataset.id);
    return (
      <GridItem key={dataset.id} metadata={dataset}>
        <Rating ratingData={ratingData} userSession={cookies["user_session"]}/>
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
