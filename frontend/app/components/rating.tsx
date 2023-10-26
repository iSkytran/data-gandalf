import { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp as solidThumbsUp, faThumbsDown as solidThumbsDown } from "@fortawesome/free-solid-svg-icons";
import { faThumbsUp as regThumbsUp, faThumbsDown as regThumbsDown } from "@fortawesome/free-regular-svg-icons";

export default function Rating({ ratingData, userSession }: { ratingData: any, userSession: string }) {
  // 0 represents no selection, 1 is positive, -1 is negative.
  const [rating, setRating] = useState(0);
  const postUrl = `/api/ratings`;
  let deleteUrl: string;
  if (ratingData !== undefined) {
    deleteUrl = `/api/ratings/${encodeURIComponent(ratingData.id)}`;
  }

  useEffect(() => {
    if (ratingData !== undefined) {
      if (ratingData.recommend === true) {
        setRating(1);
      } else if (ratingData.recommend === false) {
        setRating(-1);
      }
    }
    }, [ratingData]
  );

  const thumbsUp = () => {
    if (rating === 1) {
      setRating(0);
      fetch(deleteUrl, { method: "DELETE" });
    } else {
      setRating(1);
      fetch(postUrl, {
        method: "POST",
        body: JSON.stringify({
            recommend: true,
            user_session: userSession,
            source_dataset: ratingData.source_dataset,
            destination_dataset: ratingData.destination_dataset,
        }),
      });
    }
  };

  const thumbsDown = () => {
    if (rating === -1) {
      setRating(0);
      fetch(deleteUrl, { method: "DELETE" });
    } else {
      setRating(-1);
      fetch(postUrl, {
        method: "POST",
        body: JSON.stringify({
            recommend: true,
            user_session: userSession,
            source_dataset: ratingData.source_dataset,
            destination_dataset: ratingData.destination_dataset,
        }),
      });
    }
  };

  return (
    <>
        {rating === 1 ? (
          <FontAwesomeIcon icon={solidThumbsUp} onClick={thumbsUp}/>
        ) : (
          <FontAwesomeIcon icon={regThumbsUp} onClick={thumbsUp}/>
        )}
        {rating === -1 ? (
          <FontAwesomeIcon icon={solidThumbsDown} onClick={thumbsDown}/>
        ) : (
          <FontAwesomeIcon icon={regThumbsDown} onClick={thumbsDown}/>
        )}
    </>
  );
}
