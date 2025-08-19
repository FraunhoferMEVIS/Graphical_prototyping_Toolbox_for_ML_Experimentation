const priority = {
  Table: 0,
  'Table-Merge': 1,
  Filter: 2,
  Preprocess: 3,
  'Aggregate and Transform': 4,
  Visualize: 5,
};

export function toPriority(category: string) {
  return priority[category] ?? 999;
}
