export function formatDate(date: Date | undefined) {
  if (date) {
    return date.toISOString().substring(0, 4 + 2 + 2 + 2);
  } else {
    return "";
  }
}

export function formatCheckbox(b: boolean | undefined) {
  return b ? "on" : undefined;
}
