import FilterBar from './components/filterBar';
import Grid from './components/grid';

export default function Home() {

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <FilterBar/>
      <Grid/>
    </main>
  )
}
