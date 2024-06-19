'use server';

import styles from './page.module.css';
import { HOME_TESTS_TABLE, STRINGS } from '@/app/constants/app';
import TestsTable from '@/app/components/testsTable/testsTable';
import { getTestData } from '../../serverActions/testsTable';

const Dashboard = async ({ params: { userId } }: { params: { userId: number } }) => {
  const { HEIGHT: tableHeight, WIDTH: tableWidth } = HOME_TESTS_TABLE;

  let tests;
  try {
    tests = await getTestData();
  } catch (error) {
    console.error("Error fetching test data:", error);
    tests = [];
  }

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>Welcome to {STRINGS.TITLE}</h1>
        <p className={styles.description}>{STRINGS.DESCRIPTION}</p>
      </main>
      <TestsTable tableHeight={tableHeight} tableWidth={tableWidth} tests={tests} />
    </div>
  );
};

export default Dashboard;