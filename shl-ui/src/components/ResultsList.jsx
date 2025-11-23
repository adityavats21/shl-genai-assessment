import React from "react";
import ResultsCard from "./ResultsCard";
import Spinner from "./Spinner";

export default function ResultsList({ items, loading }) {
  if (loading)
    return (
      <div className="flex justify-center mt-12">
        <Spinner />
      </div>
    );

  if (!items.length)
    return (
      <p className="text-center mt-10 text-gray-500">
        No recommendations yet. Enter a job description above.
      </p>
    );

  return (
    <div className="max-w-4xl mx-auto mt-10 grid gap-4">
      {items.map((item, i) => (
        <ResultsCard key={i} item={item} />
      ))}
    </div>
  );
}
