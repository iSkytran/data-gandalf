import { useState, useEffect, useId } from 'react';
import Select from 'react-select';

export default function FilterBar({setSelectedTopic}: {setSelectedTopic: Function}) {
    const [topics, setTopics] = useState(null);

    useEffect(() => {
        fetch('/api/topics')
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
        let topic = selection?.value || '';
        setSelectedTopic(topic);
    };
    return (
        <div className="m-6">
            <Select instanceId={useId()} options={topics} isDisabled={!topics} isLoading={!topics} isClearable={true} onChange={selectionChange}/>
        </div>
    );
}
