import { NextResponse } from 'next/server';
import { STRINGS } from './src/app/constants/app';
import { auth } from './auth';

const protectedRoutes = Object.values(STRINGS.PAGES)
	.filter((page) => page.PROTECTED)
	.map((page) => page.PATH);

export default auth(async (req) => {
	try {
		if (!protectedRoutes.includes(req.nextUrl.pathname) || req.auth) return;
		const newUrl = new URL(STRINGS.PAGES.HOME.PATH, req.nextUrl.origin);
		newUrl.searchParams.set('callbackUrl', req.nextUrl.pathname);
		return NextResponse.redirect(newUrl);
	} catch (error) {
		console.error('Error in auth middleware:', error);
		// return NextResponse.redirect(new URL('/error', req.nextUrl.origin));
	}
});
