'use client';
import { useState } from 'react';
import FilterBar from './components/filterBar';
import Grid from './components/grid';

export default function Home() {
  let [ selectedTopic, setSelectedTopic ] = useState('');

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <FilterBar setSelectedTopic={setSelectedTopic}/>
      <Grid selectedTopic={selectedTopic} />
    </main>
  )
}
