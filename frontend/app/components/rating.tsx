import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faThumbsUp as solidThumbsUp,
  faThumbsDown as solidThumbsDown,
} from "@fortawesome/free-solid-svg-icons";
import {
  faThumbsUp as regThumbsUp,
  faThumbsDown as regThumbsDown,
} from "@fortawesome/free-regular-svg-icons";

export default function Rating({
  ratingIdx,
  ratings,
  setRatings,
}: {
  ratingIdx: number;
  ratings: any;
  setRatings: any;
}) {
  // For rating.recommend, 0 represents no selection, 1 is positive, -1 is negative.
  const rating = ratings[ratingIdx];

  const deleteRequest = () => {
    fetch(`/api/ratings/${encodeURIComponent(rating.id)}`, {
      method: "DELETE",
    });
    const newRatings = ratings.map((e: any) => {
      if (e.id === rating.id) {
        delete e.id;
        e.recommend = null;
      }
      return e;
    });
    setRatings(newRatings);
  };

  const postRequest = (recommend: boolean) => {
    rating.recommend = recommend;
    fetch("/api/ratings", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(rating),
    })
      .then((res) => res.json())
      .then((data) => {
        const newRatings = ratings.map((e: any, i: number) => {
          if (i === ratingIdx) {
            return data;
          } else {
            return e;
          }
        });
        setRatings(newRatings);
      });
  };

  const changeRating = (event: any, recommend: boolean | null) => {
    event.stopPropagation();
    if (recommend == null) {
      deleteRequest();
    } else {
      postRequest(recommend);
    }
  };

  return (
    <div className="flex space-x-1">
      {rating.recommend === true ? (
        <FontAwesomeIcon
          icon={solidThumbsUp}
          title="solid"
          size="lg"
          onClick={(e) => {
            changeRating(e, null);
          }}
        />
      ) : (
        <FontAwesomeIcon
          icon={regThumbsUp}
          title="empty"
          size="lg"
          onClick={(e) => {
            changeRating(e, true);
          }}
        />
      )}
      {rating.recommend === false ? (
        <FontAwesomeIcon
          icon={solidThumbsDown}
          title="solid"
          size="lg"
          onClick={(e) => {
            changeRating(e, null);
          }}
        />
      ) : (
        <FontAwesomeIcon
          icon={regThumbsDown}
          title="empty"
          size="lg"
          onClick={(e) => {
            changeRating(e, false);
          }}
        />
      )}
    </div>
  );
}
