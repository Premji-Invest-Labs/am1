import React from "react";

const DateTimeCellRenderer = ({ value }) => {
  if (!value) return <div>-</div>;

  // Convert UTC date to IST
  const dateObj = new Date(value);
  const istTime = new Intl.DateTimeFormat("en-IN", {
    timeZone: "Asia/Kolkata",
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  }).format(dateObj);

  return <div>{istTime}</div>;
};

export default DateTimeCellRenderer;
