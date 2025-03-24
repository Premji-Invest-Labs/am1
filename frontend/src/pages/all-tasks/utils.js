export const statuses = {
  all: "All",
  InProgress: "In Progress",
  //   paused: "On Hold",
  failed: "Failed",
};

export const statusFormatter = ({ value }) => statuses[value] ?? "";
