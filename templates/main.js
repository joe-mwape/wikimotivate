// Function to fetch and display top editors
async function fetchTopEditors() {
  const pages = [
    "Transport_in_Zambia",
    "Geography_of_Zambia",
    "List_of_populated_places_in_Zambia",
    "History_of_Zambia",
    "Ministry_of_Health_(Zambia)",
    "Education_in_Zambia",
    "Religion_in_Zambia",
    "Climate_of_Zambia",
    "National_Assembly_of_Zambia",
    "Zambia"
  ];

  const dataContainer = document.getElementById("data-container");
  dataContainer.innerHTML = ''; // Clear previous data

  for (const page of pages) {
    try {
      // Fetch top editors data from the API
      const url = `https://xtools.wmcloud.org/api/page/top_editors/en.wikipedia.org/${page}///5?nobots=true`;
      const response = await fetch(url);
      const data = await response.json();

      // Check if the data is available and has top_editors property
      if (data && data.top_editors) {
        const topEditors = data.top_editors;

        // Sort top editors by their edits count
        topEditors.sort((a, b) => b.count - a.count);

        // Assign ranks (gold, silver, bronze, honorary)
        for (let i = 0; i < topEditors.length; i++) {
          if (i === 0) topEditors[i].rank = '🥇 Gold';
          else if (i === 1) topEditors[i].rank = '🥈 Silver';
          else if (i === 2) topEditors[i].rank = '🥉 Bronze';
          else topEditors[i].rank = '🎖 Honorary';
        }

        // Create an HTML table for the top editors' information for the page
        const table = document.createElement('table');
        table.innerHTML = `
          <caption>Top Editors for ${page}</caption>
          <thead>
            <tr>
              <th>Username</th>
              <th>Edits</th>
              <th>Simple Character Edits</th>
              <th>Badge</th>
            </tr>
          </thead>
          <tbody>
            ${topEditors.slice(0, 5).map(editor => `
              <tr>
                <td>${(editor.username || 'N/A').substring(0, 10)}</td>
                <td>${editor.count || 'N/A'}</td>
                <td>${editor.minor || 'N/A'}</td>
                <td>${editor.rank || 'N/A'}</td>
              </tr>
            `).join('')}
          </tbody>
        `;

        // Add some padding to the table cells for spacing
        const cells = table.querySelectorAll('th, td');
        cells.forEach(cell => {
          cell.style.padding = '8px';
        });

        dataContainer.appendChild(table);

        // Call the createLeaderboardImageAndAutoSave function to create and automatically save the image
        await createLeaderboardImageAndAutoSave(page, data);
        // Add an empty line to separate pages
        dataContainer.innerHTML += '<br>';
      } else {
        dataContainer.innerHTML += `No top editors data available for ${page}<br>`;
      }
    } catch (error) {
      dataContainer.innerHTML += `Error fetching data for ${page}: ${error.message}<br>`;
    }
  }
}

// Function to create a leaderboard image and automatically save it
async function createLeaderboardImageAndAutoSave(pageName, topEditorsData) {
  const topEditors = topEditorsData.top_editors || [];

  if (topEditors.length > 0) {
    const leaderboardList = [];
    let maxUsernameLength = 0;

    topEditors.forEach((editor, idx) => {
      const username = editor.username || 'N/A';
      let rank = 'Honorary'; // Default rank

      if (idx === 0) rank = '🥇 Gold';
      else if (idx === 1) rank = '🥈 Silver';
      else if (idx === 2) rank = '🥉 Bronze';

      const count = editor.count || 'N/A';
      const minor = editor.minor || 'N/A';

      leaderboardList.push({ username, count, minor, rank });

      // Track the length of the longest username
      maxUsernameLength = Math.max(maxUsernameLength, username.length);
    });

    // Calculate cell width based on the length of the longest username
    const cellWidth = Math.max(120, maxUsernameLength * 10); // Minimum width of 120 pixels

    // Create the leaderboard image
    const tableWidth = cellWidth * 4;
    const tableHeight = 30 * (leaderboardList.length + 1);
    const background = 'rgb(255, 255, 255)';
    const headerColor = 'rgb(200, 200, 200)';
    const rowColors = ['rgb(255, 165, 0)', 'rgb(169, 169, 169)', 'rgb(139, 69, 19)'];
    const textColor = 'rgb(0, 0, 0)';
    const font = '16px Arial';

    const canvas = document.createElement('canvas');
    canvas.width = tableWidth;
    canvas.height = tableHeight;
    const context = canvas.getContext('2d');

    // Draw the header
    context.fillStyle = headerColor;
    context.fillRect(0, 0, tableWidth, 30);
    context.fillStyle = textColor;
    context.font = font;
    context.fillText('Contributor', 5, 20);
    context.fillText('Count', cellWidth + 10, 20);
    context.fillText('Minor', 2 * cellWidth + 5, 20);
    context.fillText('Rank', 3 * cellWidth + 5, 20);

    leaderboardList.forEach((entry, i) => {
      const rowColor = i < 3 ? rowColors[i % rowColors.length] : background;

      // Draw rows
      context.fillStyle = rowColor;
      context.fillRect(0, (i + 1) * 30, tableWidth, (i + 2) * 30);

      // Draw text
      context.fillStyle = textColor;
      context.font = font;
      context.fillText(entry.username, 5, (i + 1) * 30 + 20);
      context.fillText(entry.count.toString(), cellWidth + 10, (i + 1) * 30 + 20);
      context.fillText(entry.minor.toString(), 2 * cellWidth + 5, (i + 1) * 30 + 20);
      context.fillText(entry.rank, 3 * cellWidth + 5, (i + 1) * 30 + 20);
    });

    // Save the leaderboard image with the page title in the filename
    const imageFileName = `${pageName.replace(/ /g, '_')}_leaderboard_image.png`;

    // Convert the canvas to a Blob
   // canvas.toBlob((blob) => {
     // const url = window.URL.createObjectURL(blob);

      // Create a temporary link to trigger the download
     // const link = document.createElement('a');
    //  link.href = url;
     // link.download = imageFileName;

      // Programmatically click the link to trigger the download
    //  link.click();

      // Clean up
    //  window.URL.revokeObjectURL(url);
   // }, 'image/png');

    // No need to return the generated image filename in this version
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const runButton = document.getElementById('run-button');
  const dataContainer = document.getElementById('data-container');

  runButton.addEventListener('click', async () => {
    runButton.disabled = true;
    runButton.innerHTML = 'Fetching top editors...';

    try {
      await fetchTopEditors();
    } catch (error) {
      dataContainer.innerHTML = `An error occurred: ${error.message}`;
    } finally {
      runButton.disabled = false;
      runButton.innerHTML = 'Run Top Editors';
    }
  });
});


