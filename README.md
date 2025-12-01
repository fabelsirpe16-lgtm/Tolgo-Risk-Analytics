\# Tolgo – Risk \& Anomaly Detection (Fintech Analytics)

\### Transaction Monitoring • Operational Risk • Python (pandas)



This project simulates a simplified version of transaction monitoring and 

risk analytics performed in a fintech environment.



It is inspired by operational tasks common in digital payments:

\- Mobile Money transactions  

\- Virtual prepaid cards  

\- User behaviour monitoring  

\- Early detection of abnormal patterns  

\- Basic KYC / AML rule-based checks  



The objective is to reproduce a \*\*credible risk-analytics workflow\*\* suitable for 

analyst roles in fintech, banking, or investment institutions.



---



**## Repository Structure**



```

Tolgo-Risk-Analytics/

│

├── Data/

│   ├── transactions.csv          ← Synthetic fintech dataset

│   └── transactions\_scored.csv   ← Output with anomaly flags

│

├── Scripts/

│   ├── generate\_dataset.py       ← Generates synthetic transactions

│   ├── detect\_anomalies.py       ← Rule-based anomaly scoring

│   └── utils.py                  ← KPI \& risk analytics functions

│

├── notebooks/

│   └── Tolgo\_Anomaly\_Risk\_Analysis.ipynb

│

└── README.md

```



Each component mirrors the modular structure of a real analytical pipeline.



---



\## **Dataset Overview**



The dataset includes \*\*1,000+ fintech-like transactions\*\*, designed to mimic:



\- multiple users  

\- top-ups \& payments  

\- payment methods (card, mobile money, bank transfer)  

\- realistic timestamps  

\- manually injected anomalies:

&nbsp; - unusually large payments  

&nbsp; - rapid consecutive transactions  

&nbsp; - repeated top-ups within short intervals  



\### \*\*Columns\*\*



| Column | Description |

|--------|-------------|

| transaction\_id | Unique transaction identifier |

| user\_id | Unique user identifier |

| amount | Transaction amount |

| time | Timestamp |

| method | Payment method |

| topup\_flag | Whether the transaction is a top-up |



---



**## Risk Rules \& Anomaly Detection**



The anomaly detection pipeline uses \*\*three rule-based indicators\*\* commonly employed

in fintech operational risk:



\### **Amount Outliers (Z-Score)**

Detects unusually large transactions using statistical deviation.



\### **Rapid Consecutive Transactions (< 60 sec)**

Flags multiple transactions executed in very short intervals.



\### **Frequent Top-Ups (Rolling 3-Windows)**

Identifies repeated top-up events in short time windows.



\### **Final Score**



```python

is\_anomaly = 1 if (amount\_flag + rapid\_flag + freq\_flag) >= threshold else 0

```



This produces a binary anomaly classification.



---



**## Visualizations (Notebook)**



The notebook provides:



\- Exploratory data analysis  

\- KPI metrics (via utils.py)  

\- Visualization of flagged anomalies  

\- Time-based transaction dynamics  

\- User-level insights  

\- Export of the final scored dataset  



\*\*Example visualization:\*\*



\- Scatter plot of transaction \*\*amount vs time\*\*  

\- Color-coded by anomaly status:  

&nbsp; - \*\*Blue = normal\*\*  

&nbsp; - \*\*Red = anomaly\*\*



---



**## Utility Functions (utils.py)**



`utils.py` includes reusable business KPIs such as:



\- Total revenue  

\- Average transaction value  

\- User transaction frequency  

\- Top users by amount or volume  

\- Daily and hourly activity  

\- Top-up rate \& distribution  

\- Cohort-like earliest transaction metrics  

\- Anomaly rate \& risk drivers  



These metrics mirror real fintech and digital-payments analytics practices.



---



**## How to Run the Project**



\### \*\*1. Generate the dataset\*\*

```bash

python Scripts/generate\_dataset.py

```



\### \*\*2. Run anomaly detection\*\*

```bash

python Scripts/detect\_anomalies.py

```



\### \*\*3. Open the notebook\*\*

```bash

notebooks/Tolgo\_Anomaly\_Risk\_Analysis.ipynb

```



\### \*\*4. (Optional) Use util functions\*\*

Inside the notebook:



```python

import sys

sys.path.append("../Scripts")



from utils import \*

total\_revenue(df)

```



---



**## Purpose of this Project**



This project demonstrates:



\- Ability to structure a complete analytics workflow  

\- Understanding of fintech transaction behaviour  

\- Practical rule-based anomaly detection  

\- Clean, modular Python code  

\- Use of reusable analytics functions (utils.py)  

\- Ability to communicate findings through notebooks  

\- Readiness for Analyst roles (Risk, Finance, Data, Fintech)  



---



**## Author**



**Fabel Sirpe**

LinkedIn: https://www.linkedin.com/in/fabel-sirpe-0275421b3



