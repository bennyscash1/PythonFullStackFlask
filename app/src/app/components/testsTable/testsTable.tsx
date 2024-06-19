'use client';

import Link from 'next/link';
import React from 'react';
import styles from './testsTable.module.css';
import { runTest, deleteTest } from '@/app/serverActions/testsTable';

export interface Test {
  testName: string;
}

interface TestTableProps {
  tableHeight: string;
  tableWidth: string;
  tests: Test[];
}

const TestTable = ({ tableHeight, tableWidth, tests }: TestTableProps) => {
  return (
    <table className={styles.table} style={{height: tableHeight, width: tableWidth }}>
      <thead>
        <tr>
          {['Type', 'Name', 'Edit', 'Run', 'Delete'].map((column, index) => (<th key={index}>{column}</th>))}
        </tr>
      </thead>
      <tbody>
        {tests.map((test, index) => (
          <tr key={index}>
            <td>Web Test</td>
            <td>{test.testName}</td>
            <td>
                <Link href={
                  {
                    pathname:'/webTemplates/editTest',
                    query: { testName: test.testName }
                  }
                }>
                  <button type='button' className={styles.editBtn}>Edit</button>
                </Link>
            </td>
            <td>
              <button type='button' className={styles.runBtn} onClick={() => runTest(test.testName)}>Run</button>
            </td>
            <td>
              <button type='button' className={styles.deleteBtn} onClick={() => deleteTest(test.testName) }>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TestTable;
