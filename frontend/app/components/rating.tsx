import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp as solidThumbsUp, faThumbsDown as solidThumbsDown } from "@fortawesome/free-solid-svg-icons";
import { faThumbsUp as regThumbsUp, faThumbsDown as regThumbsDown } from "@fortawesome/free-regular-svg-icons";
import { useCookies } from "react-cookie";
import { v4 as uuidv4 } from "uuid";

export default function Rating({ metadata }: { metadata: any }) {
  // 0 represents no selection, 1 is positive, -1 is negative.
  const [rating, setRating] = useState(0);
  const [cookies, setCookie] = useCookies(["session-uuid"]);
  // if (!cookies.some((e: any) => e.name === "session-uuid"])) {
  //   setCookie("session-uuid", uuidv4());
  // }
  // const url = `/api/datasets/${encodeURIComponent(params.dataset)}`;
  

  const thumbsUp = () => {
    if (rating === 1) {
      setRating(0);
      // fetch(url, { method: "DELETE" });
    } else {
      setRating(1);
    }
  };

  const thumbsDown = () => {
    if (rating === -1) {
      setRating(0);
      // fetch(url, { method: "DELETE" });
    } else {
      setRating(-1);
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
