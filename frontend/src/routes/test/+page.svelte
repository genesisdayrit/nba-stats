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

{#if error}
  <p class="text-red-500">{error}</p>
{:else if data.length > 0}
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200 border-collapse">
      <thead class="bg-gray-50">
        <tr>
          {#each columns as column}
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-200">{column}</th>
          {/each}
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each data as row}
          <tr class="hover:bg-gray-100">
            {#each columns as column}
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 border-b border-gray-200">{row[column]}</td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
{:else}
  <p>No data available</p>
{/if}

