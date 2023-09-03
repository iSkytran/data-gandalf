// `app/dashboard/page.tsx` is the UI for the `/dashboard` URL
export default async function Page() {
    const data = await getData();
    return <h1>From the server, we got: {data} </h1>
}

async function getData() {
    const res = await fetch('http://localhost:8080')
    // The return value is *not* serialized
    // You can return Date, Map, Set, etc.
   
    if (!res.ok) {
      // This will activate the closest `error.js` Error Boundary
      throw new Error('Failed to fetch data')
    }
   
    return res.json()
  }