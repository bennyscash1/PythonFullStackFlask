"use client"

import styles from './page.module.css';
import { HOME_TESTS_TABLE, STRINGS } from '@/app/constants/app';
import TestsTable from '@/app/components/testsTable/testsTable';
import { useTests } from './hooks/useTests';

const HomePage = () => {
  const {tests, runTest, deleteTest} = useTests();

  const {HEIGHT: tableHeight, WIDTH: tableWidth} = HOME_TESTS_TABLE;
  
  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>Welcome to {STRINGS.TITLE}</h1>
        <p className={styles.description}>{STRINGS.DESCRIPTION}</p>
      </main>
      <TestsTable tests={tests} runTest={runTest} deleteTest={deleteTest} tableHeight={tableHeight} tableWidth={tableWidth}/>
    </div>
  );
};

export default HomePage;