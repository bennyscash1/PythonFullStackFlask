export function GET() {
	// const res = await fetch('https://data.mongodb-api.com/...', {
	// 	next: { revalidate: 60 }, // Revalidate every 60 seconds
	// });
	// const data = await res.json();

	return Response.json('HELLO WORLD');
}
