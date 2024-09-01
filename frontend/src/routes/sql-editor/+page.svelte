<!-- src/routes/sql-editor/+page.svelte -->
<script>
  import { writable } from 'svelte/store';

  let sqlQuery = '';
  let results = writable([]);
  let columns = writable([]);
  let error = writable('');

  // Function to run the SQL query
  async function runQuery() {
    try {
      const response = await fetch('/editor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: sqlQuery }),
      });

      if (!response.ok) {
        throw new Error('Failed to execute query.');
      }

      const data = await response.json();

      if (data.success) {
        results.set(data.data);
        if (data.data.length > 0) {
          columns.set(Object.keys(data.data[0]));
        }
      } else {
        throw new Error(data.error);
      }
    } catch (err) {
      error.set(err.message);
    }
  }

  // Function to handle tab key for indentation in the textarea
  function handleTab(event) {
    if (event.key === 'Tab') {
      event.preventDefault();
      const start = event.target.selectionStart;
      const end = event.target.selectionEnd;

      // Set textarea value to: text before caret + tab + text after caret
      sqlQuery = sqlQuery.substring(0, start) + '\t' + sqlQuery.substring(end);

      // Put caret at right position again
      event.target.selectionStart = event.target.selectionEnd = start + 1;
    }
  }
</script>

<style>
  .editor {
    width: 100%;
    height: 150px;
    font-family: monospace;
    font-size: 16px;
    margin-bottom: 20px;
    border: 1px solid #ccc; /* Added border for visibility */
    background-color: #f9f9f9; /* Added background color */
  }

  button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border: 1px solid #333; /* Added border for visibility */
    background-color: #007bff; /* Button color */
    color: #fff; /* Button text color */
  }

  .result-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  .result-table th,
  .result-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }

  .result-table th {
    background-color: #f2f2f2;
  }

  .text-red-500 {
    color: #f56565; /* Red color for error text */
  }
</style>

<h1>NBA Dataset SQL Query Editor</h1>
<p>Enter your SQL query below to interact with the NBA dataset.</p>

<textarea
  class="editor"
  bind:value={sqlQuery}
  placeholder="SELECT * FROM players WHERE team = 'Lakers';"
  on:keydown={handleTab}
/>

<button on:click={runQuery}>Run Query</button>

{#if $error}
  <p class="text-red-500">Error: {$error}</p>
{:else if $results.length > 0}
  <!-- Display number of results -->
  <p>{`Results returned: ${$results.length}`}</p>
  <table class="result-table">
    <thead>
      <tr>
        {#each $columns as column}
          <th>{column}</th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each $results as result}
        <tr>
          {#each $columns as column}
            <td>{result[column]}</td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
{:else}
  <p>No results to display. Please run a query.</p>
{/if}

