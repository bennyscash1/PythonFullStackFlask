import { useState, useRef, useEffect } from "react";
import { Test } from "../components/testsTable/testsTable";

export const useTests = () => {
  const [tests, setTests] = useState<Test[]>([]);
  const fetchedTestsRef = useRef<Test[]>([]);

  useEffect(() => {
    const fetchTests = async () => {
      console.log('getting tests')
      try{
        const res = await fetch('http://127.0.0.1:5000/tests') 
        const data = await res.json()
        console.log('data:', data)
        if (JSON.stringify(data) !== JSON.stringify(fetchedTestsRef.current)) {
          console.log('setting tests')
          fetchedTestsRef.current = data;
          setTests(data)
        }
      } catch (error) {
        console.error('Error fetching tests:', error)
      }
    }

    fetchTests()
  }, []);

  const runTest = async (testName: string) => {
    try {
      const response = await fetch('/api/runTest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ testName }),
      });

      const data = await response.json();
      if (data.error) {
        alert(`Failed to run test: ${data.error}`);
      } else {
        alert('Test run successfully!');
      }
    } catch (error) {
      console.error('Error running test:', error);
    }
  };

  const deleteTest = async (testName: string) => {
    try {
      const response = await fetch(`/api/delete/${testName}`, {
        method: 'DELETE',
      });

      const data = await response.json();
      if (data.success) {
        setTests(tests.filter(test => test.testName !== testName));
      } else {
        alert(`Failed to delete test: ${data.error}`);
      }
    } catch (error) {
      console.error('Error deleting test:', error);
    }
  };

  return { tests, runTest, deleteTest};
};