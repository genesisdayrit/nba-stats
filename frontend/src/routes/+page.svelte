<!-- src/routes/editor/+page.svelte -->
<script>
  let sqlQuery = '';
  let results = [];

  // Mock function to simulate query execution
  function runQuery() {
    // Example: Hardcoded results for demonstration purposes
    results = [
      { player: 'LeBron James', team: 'Lakers', points: 27 },
      { player: 'Stephen Curry', team: 'Warriors', points: 30 },
      { player: 'Kevin Durant', team: 'Nets', points: 28 }
    ];
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

<h1>NBA Dataset Query Editor</h1>
<p>Enter your SQL query below to interact with the NBA dataset.</p>

<textarea
  class="editor"
  bind:value={sqlQuery}
  placeholder="SELECT * FROM players WHERE team = 'Lakers';"
/>

<button on:click={runQuery}>Run Query</button>

{#if results.length > 0}
  <table class="result-table">
    <thead>
      <tr>
        <th>Player</th>
        <th>Team</th>
        <th>Points</th>
      </tr>
    </thead>
    <tbody>
      {#each results as result}
        <tr>
          <td>{result.player}</td>
          <td>{result.team}</td>
          <td>{result.points}</td>
        </tr>
      {/each}
    </tbody>
  </table>
{:else}
  <p>No results to display. Please run a query.</p>
{/if}

