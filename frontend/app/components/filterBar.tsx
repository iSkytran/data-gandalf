import { useState, useEffect, useId } from "react";
import Select from "react-select";

export default function FilterBar({
  className,
  setSelectedTopic,
}: {
  className: string;
  setSelectedTopic: Function;
}) {
  const [topics, setTopics] = useState(null);

  useEffect(() => {
    fetch("/api/topics")
      .then((res) => res.json())
      .then((data) => {
        let options: Array<object> = [];
        data.forEach((topic: string) => {
          options.push({ value: topic, label: topic });
        });
        setTopics(options);
      });
  }, []);

  let selectionChange = (selection: Array<object>) => {
    let topic = selection?.value || "";
    setSelectedTopic(topic);
  };
  return (
    <Select
      className={className + ' topicSelect'}
      placeholder="Filter by Topic"
      instanceId={useId()}
      options={topics}
      isDisabled={!topics}
      isLoading={!topics}
      isClearable={true}
      onChange={selectionChange}
    />
  );
}
