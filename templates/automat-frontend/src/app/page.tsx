"use client"

import styles from './page.module.css';
import { STRINGS } from './constants';
import TestsTable from '@/app/components/testsTable/testsTable';
import { useTests } from './hooks/useTests';

const HomePage = () => {
  const {tests, runTest, deleteTest} = useTests();
  
  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>Welcome to {STRINGS.TITLE}</h1>
        <p className={styles.description}>{STRINGS.DESCRIPTION}</p>
      </main>
      <TestsTable tests={tests} runTest={runTest} deleteTest={deleteTest} tableHeight="75%" tableWidth="87%"/>
    </div>
  );
};

export default HomePage;