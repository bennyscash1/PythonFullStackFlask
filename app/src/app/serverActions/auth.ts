'use server';

import { signOut, signIn } from '../../../auth';

export const signOutAction = async () => {
	await signOut();
};

export const signInAction = async () => {
	await signIn();
};
