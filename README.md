### **Batch Deletion App for Clearing Large Tables**

#### **Overview**
This application is designed to efficiently delete large amounts of data
from MySQL tables in batches. It provides a safe, interactive, and
user-friendly interface for managing large table cleanup tasks, ensuring
minimal performance impact on your database.

---

#### **Key Benefits**

#### **1. Optimized for Performance**
- Deletes data in **manageable batches**, preventing long locks and
reducing the risk of overloading the database.
- Ensures consistent performance by committing smaller transactions.

#### **2. Interactive Interface**
- Powered by **Streamlit**, the app provides a simple and intuitive
interface for users to:
   - Specify the table and column for deletion.
   - Define date ranges for targeted deletions.
   - Configure batch sizes for optimal performance.

#### **3. Real-Time Monitoring**
- Displays real-time progress, including the number of rows deleted in
each batch and the total rows deleted.
- Provides clear feedback on the deletion process, ensuring full
transparency.

#### **4. Safe and Error-Resilient**
- Includes robust error handling to gracefully recover from issues
during the deletion process.
- Ensures database connections and resources are properly managed and
released.

#### **5. Flexibility and Control**
- Allows users to:
   - Target specific date ranges for deletion using the `TIMESTAMP`
column.
   - Adjust batch sizes dynamically based on the database's performance.
   - Specify custom schemas and tables for deletion tasks.

---

#### **Use Cases**
- **Clearing Old Logs or Records**: Remove outdated records from large
log tables to improve query performance and save storage.
- **Archiving and Housekeeping**: Selectively delete data within
specific date ranges to maintain database cleanliness.
- **Safe Cleanup During Production**: Manage deletions without risking
downtime or affecting other queries.

---

#### **How It Works**
1. **Connect to the Database**:
    - Enter your database credentials, including host, user, password,
and database name.

2. **Configure Deletion Parameters**:
    - Specify the schema, table, and column for deletion.
    - Define the date range and batch size.

3. **Run the Deletion Process**:
    - Monitor progress in real-time as rows are deleted in batches.
    - Receive success and error notifications directly in the app.
