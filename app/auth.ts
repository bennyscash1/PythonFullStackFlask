import NextAuth, { type NextAuthConfig } from 'next-auth';
// import { cert } from 'firebase-admin/app';
// import { FirestoreAdapter } from '@auth/firebase-adapter';
import Google from 'next-auth/providers/google';

const GOOGLE_CLIENT_ID = process.env.AUTH_GOOGLE_ID;
const GOOGLE_CLIENT_SECRET = process.env.AUTH_GOOGLE_SECRET;
// const FIREBASE_PROJECT_ID = process.env.AUTH_FIREBASE_PROJECT_ID;
// const FIREBASE_CLIENT_EMAIL = process.env.AUTH_FIREBASE_CLIENT_EMAIL;
// const FIREBASE_PRIVATE_KEY = process.env.AUTH_FIREBASE_PRIVATE_KEY;
const AUTH_SECRET = process.env.AUTH_SECRET;

const authConfig: NextAuthConfig = {
	providers: [
		Google({
			clientId: GOOGLE_CLIENT_ID,
			clientSecret: GOOGLE_CLIENT_SECRET,
			authorization: {
				params: {
					prompt: 'consent',
					access_type: 'offline',
					response_type: 'code',
				},
			},
		}),
	],
	// adapter: FirestoreAdapter({
	// 	credential: cert({
	// 		projectId: FIREBASE_PROJECT_ID,
	// 		clientEmail: FIREBASE_CLIENT_EMAIL,
	// 		privateKey: FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
	// 	}),
	// }),
	secret: AUTH_SECRET,
	session: { strategy: 'jwt' },
};

export const { auth, handlers, signIn, signOut } = NextAuth(authConfig);
