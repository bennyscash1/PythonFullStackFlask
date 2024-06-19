'use server';

import { revalidateTag } from 'next/cache';

export const getTestData = async () => {
	console.log('getting tests');
	try {
		const res = await fetch('http://127.0.0.1:5000/tests', {
			next: { tags: ['testData'] },
		});
		const data = await res.json();
		return data;
	} catch (error) {
		console.error('Error fetching tests:', error);
		return [];
	}
};

const validateTestName = (testName: string) =>
	testName && testName.match(/^[a-zA-Z0-9_]+$/) !== null;

export const runTest = async (testName: string) => {
	if (!validateTestName(testName)) {
		console.error('Invalid test name:', testName);
		return;
	}
	console.log('running test', testName);
	try {
		const response = await fetch('http://127.0.0.1:5000/runTest', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ testName }),
		});

		const data = await response.json();
		if (data.error) {
			console.log(`Failed to run test: ${data.error}`);
		} else {
			console.log('Test run successfully!');
		}
	} catch (error) {
		console.error('Error running test:', error);
	}
};

export const deleteTest = async (testName: string) => {
	if (!validateTestName(testName)) {
		console.error('Invalid test name:', testName);
		return;
	}
	try {
		const response = await fetch(`/api/delete/${testName}`, {
			method: 'DELETE',
		});

		const data = await response.json();
		if (data.success) {
			revalidateTag('testData');
			location.reload();
		} else {
			alert(`Failed to delete test: ${data.error}`);
		}
	} catch (error) {
		console.error('Error deleting test:', error);
	}
};
