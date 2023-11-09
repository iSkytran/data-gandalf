import { titleCase } from "title-case";

export const processMetadata = (dataset: any) => {
  dataset.title = dataset.title.replace(/,/g, ", ");
  dataset.topic = dataset.topic.replace(/,/g, ", ");
  dataset.licenses = dataset.licenses.replace(/,/g, ", ");
  dataset.tags = dataset.tags.replace(/,/g, ", ");
  dataset.title = titleCase(dataset.title);
  dataset.topic = titleCase(dataset.topic);
  dataset.licenses = titleCase(dataset.licenses);
  dataset.tags = titleCase(dataset.tags);
  return dataset;
};
