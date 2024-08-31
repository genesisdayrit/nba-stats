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
</script>

<style>
  .editor {
    width: 100%;
    height: 150px;
    font-family: monospace;
    font-size: 16px;
    margin-bottom: 20px;
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
</style>

<h1>NBA Dataset SQL Query Editor</h1>
<p>Enter your SQL query below to interact with the NBA dataset.</p>

<textarea
  class="editor"
  bind:value={sqlQuery}
  placeholder="SELECT * FROM players WHERE team = 'Lakers';"
/>

<button on:click={runQuery}>Run Query</button>

{#if $error}
  <p class="text-red-500">Error: {$error}</p>
{:else if $results.length > 0}
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

