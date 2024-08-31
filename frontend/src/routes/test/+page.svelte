<!-- src/routes/test/+page.svelte -->
<script>
  import { onMount } from 'svelte';
  let data = [];
  let error = null;

  // Fetch data from the API endpoint on component mount
  onMount(async () => {
    try {
      const response = await fetch('/test');
      const result = await response.json();
      if (result.success) {
        data = result.data;
      } else {
        error = result.error;
      }
    } catch (err) {
      error = 'Failed to fetch data from the API';
      console.error(err);
    }
  });
</script>

{#if error}
  <p>Error: {error}</p>
{:else}
  <table>
    <thead>
      <tr>
        <th>Game Date</th>
        <th>Matchup</th>
        <th>WL</th>
        <th>Min</th>
        <th>PTS</th>
        <!-- Add more columns as needed -->
      </tr>
    </thead>
    <tbody>
      {#each data as game}
        <tr>
          <td>{game.game_date}</td>
          <td>{game.matchup}</td>
          <td>{game.wl}</td>
          <td>{game.min}</td>
          <td>{game.pts}</td>
          <!-- Add more table data as needed -->
        </tr>
      {/each}
    </tbody>
  </table>
{/if}

