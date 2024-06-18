'use client'

import { useState } from "react";
import styles from "./page.module.css";

const MobileTestPage = () => {
    const [fieldPairs, setFieldPairs] = useState(0);

    const addFieldPair = () => {
        setFieldPairs(fieldPairs + 1);
    }

    const addXpathField = () => {}

    const addXpathAssert = () => {}

  return (
    <div className={styles.page}>
        <h1 className={styles.title}>Mobile Test</h1>
        <form method="post">
            <label htmlFor="appPackage">App Package:</label>
            <input type="text" id="appPackage" name="appPackage" required></input><br></br>

            <label htmlFor="appActivity">App Activity:</label>
            <input type="text" id="appActivity" name="appActivity" required></input><br></br>

            <label htmlFor="udid">UDID:</label>
            <input type="text" id="udid" name="udid" required></input><br></br>

            <div id="dynamic-fields">    
                {[...Array(fieldPairs)].map((_, index) => (
                    <div key={index} className="field-pair">
                        <label htmlFor={`xpathField${index}`}>Input field locator:</label>
                        <input type='text' id={`xpathField${index}`} name={`xpathField${index}`}></input>
                        <label htmlFor={`inputField${index}`}>Input:</label>
                        <input type='text' id={`inputField${index}`}></input>
                    </div>
                ))}
            </div>

            <button type="button" onClick={addFieldPair}>Add Input field</button>
            <button type="button" onClick={addXpathField}>Add button click</button>
            <button type="button" onClick={addXpathAssert}>Add locator assert</button><br></br>

            <input type="submit" className="submit-button" value="Run Test"></input>
        </form>
       
        <div id="test-result">
            {/* {{ result|safe }} */}
        </div>
    </div>
  );
};

export default MobileTestPage;