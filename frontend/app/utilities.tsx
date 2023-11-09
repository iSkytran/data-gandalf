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
  dataset.topicStyle = hashToStyle(hashCode(dataset.topic));
  return dataset;
};

export const hashCode = (str: string) => {
    let hash = 0;
    for (let i = 0, len = str.length; i < len; i++) {
        let chr = str.charCodeAt(i);
        hash = (hash << 5) - hash + chr;
        hash |= 0;
    }
    return Math.abs(hash);
};

export const hashToStyle = (hash: number) => {
  const hue = hash % 360;
  const background = `hsl(${hue}, 50%, 90%)`;
  const text = `hsl(${hue}, 50%, 20%)`;
  const border = `hsl(${hue}, 50%, 35%)`;

  const style = {
    backgroundColor: background,
    color: text,
    borderColor: border,
  };

  return style;
};
