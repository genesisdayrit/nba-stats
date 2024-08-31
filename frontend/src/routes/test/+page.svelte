<!-- src/routes/test/+page.svelte -->
<script>
  import { onMount } from 'svelte';
  let data = [];
  let columns = [];
  let error = null;

  // Fetch data from the API endpoint on component mount
  onMount(async () => {
    try {
      const response = await fetch('/test');
      const result = await response.json();
      if (result.success) {
        data = result.data;

        // Automatically generate column headers from the keys of the first object
        if (data.length > 0) {
          columns = Object.keys(data[0]);
        }
      } else {
        error = result.error;
      }
    } catch (err) {
      error = 'Failed to fetch data from the API';
      console.error(err);
    }
  });
</script>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }

  th {
    background-color: #f4f4f4;
  }

  tr:nth-child(even) {
    background-color: #f9f9f9;
  }

  tr:hover {
    background-color: #f1f1f1;
  }
</style>

{#if error}
  <p>Error: {error}</p>
{:else if data.length > 0}
  <table>
    <thead>
      <tr>
        {#each columns as column}
          <th>{column}</th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each data as row}
        <tr>
          {#each columns as column}
            <td>{row[column]}</td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
{:else}
  <p>No data available</p>
{/if}

