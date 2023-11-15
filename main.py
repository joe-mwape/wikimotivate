from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import facebook
import requests

# Facebook App credentials
APP_ID = '238449675721641'
APP_SECRET = '45de0dcbf92b39c33310e7773638c972'
ACCESS_TOKEN = 'EAADY3mQ326kBOZBda151buaSwTpmhi2XqTQChcZA4w6MhKwA6U4BpoY3n19KOv5jZBfIvlEmXeRVkDsXjnRKFNHl6fxp43s1xJo1waUWvEpoByuFc6LrE4lMoURHxZBgbC5J0ZAwbJLGZAaPKNuXLuqHu6Oqap0akQs9hxT2VZC6WIBq7edmjmv98JqEohQVZBVOOBV8Wa4ZD'

# Function to get top editors for a Wikipedia page using the provided API
def get_top_editors(page_name):
    url = f'https://xtools.wmcloud.org/api/page/top_editors/en.wikipedia.org/{page_name}///5?nobots=true'

    try:
        response = requests.get(url, timeout=None)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to create and save a leaderboard image for a Wikipedia page
def create_leaderboard_image(page_name, top_editors_data):
    top_editors = top_editors_data.get('top_editors', [])

    if top_editors:
        # Create a leaderboard list
        leaderboard_list = []
        max_username_length = 0

        for idx, editor in enumerate(top_editors, start=1):
            username = editor.get("username", "N/A")
            rank = ""
            if idx == 1:
                rank = "Gold"  # Gold rank
            elif idx == 2:
                rank = "Silver"  # Silver rank
            elif idx == 3:
                rank = "Bronze"  # Bronze rank
            else:
                rank = "Honorary"  # Honorary rank
            total_edits = editor.get("count", 0)  # Change label from "count" to "total edits"
            minor_edits = editor.get("minor", 0)  # Change label from "minor" to "minor edits"
            leaderboard_list.append((username, total_edits, minor_edits, rank))

            # Track the length of the longest username
            max_username_length = max(max_username_length, len(username))

        # Calculate cell width based on the length of the longest username
        cell_width = max(120, max_username_length * 10)  # Minimum width of 120 pixels

        # Create the leaderboard image
        table_width = cell_width * 4
        table_height = 30 * (len(leaderboard_list) + 1)
        background_color = (255, 255, 255)
        header_color = (200, 200, 200)
        row_colors = [(255, 165, 0), (169, 169, 169), (139, 69, 19)]
        text_color = (0, 0, 0)
        font = ImageFont.truetype('arial.ttf', 16)  # Use the Arial font

        leaderboard_image = Image.new('RGB', (table_width, table_height), background_color)
        draw = ImageDraw.Draw(leaderboard_image)

        draw.rectangle([(0, 0), (table_width, 30)], fill=header_color)
        draw.text((5, 5), 'Contributor', fill=text_color, font=font)
        draw.text((cell_width + 10, 5), 'Total Edits', fill=text_color, font=font)  # Change label from "Count" to "Total Edits"
        draw.text((2 * cell_width + 5, 5), 'Minor Edits', fill=text_color, font=font)  # Change label from "Minor" to "Minor Edits"
        draw.text((3 * cell_width + 5, 5), 'Rank', fill=text_color, font=font)

        for i, (contributor, total_edits, minor_edits, rank) in enumerate(leaderboard_list):
            if i < 3:
                row_color = row_colors[i % len(row_colors)]
            else:
                row_color = background_color
            draw.rectangle([(0, (i + 1) * 30), (table_width, (i + 2) * 30)], fill=row_color)
            draw.text((5, (i + 1) * 30 + 5), contributor, fill=text_color, font=font)
            draw.text((cell_width + 10, (i + 1) * 30 + 5), str(total_edits), fill=text_color, font=font)  # Change label from "count" to "total edits"
            draw.text((2 * cell_width + 5, (i + 1) * 30 + 5), str(minor_edits), fill=text_color, font=font)  # Change label from "minor" to "minor edits"
            draw.text((3 * cell_width + 5, (i + 1) * 30 + 5), rank, fill=text_color, font=font)

        # Save the leaderboard image with the page title in the filename
        image_path = f'{page_name.replace(" ", "_")}_leaderboard_image.png'
        leaderboard_image.save(image_path)
        return image_path
    else:
        return None

# Function to post the leaderboard image and message on Facebook
def post_leaderboard_on_facebook(page_name, image_path, top_editors_data):
    page_access_token = 'EAADY3mQ326kBOZBda151buaSwTpmhi2XqTQChcZA4w6MhKwA6U4BpoY3n19KOv5jZBfIvlEmXeRVkDsXjnRKFNHl6fxp43s1xJo1waUWvEpoByuFc6LrE4lMoURHxZBgbC5J0ZAwbJLGZAaPKNuXLuqHu6Oqap0akQs9hxT2VZC6WIBq7edmjmv98JqEohQVZBVOOBV8Wa4ZD'  # Replace with your actual Facebook page access token
    graph = facebook.GraphAPI(page_access_token)

    top_editors = top_editors_data.get('top_editors', [])

    # Create a link to the top editors page section
    top_editors_link = f'https://xtools.wmcloud.org/articleinfo/en.wikipedia.org/{page_name.replace(" ", "_")}#top-editors'

    post_message = f"Leaderboard for {page_name}:\n\n"
    post_message += f"Top Editors: {top_editors_link}\n\n"

    for idx, editor in enumerate(top_editors, start=1):
        username = editor.get("username", "N/A")
        total_edits = editor.get("count", 0)  # Change label from "count" to "total edits"
        minor_edits = editor.get("minor", 0)  # Change label from "minor" to "minor edits"
        rank = ""
        if idx == 1:
            rank = "Gold"  # Gold rank
        elif idx == 2:
            rank = "Silver"  # Silver rank
        elif idx == 3:
            rank = "Bronze"  # Bronze rank
        else:
            rank = "Honorary"  # Honorary rank
        post_message += f"{rank} {username}: Total Edits - {total_edits}, Minor Edits - {minor_edits}\n"

    page_id = '102776269561207'  # Replace with your actual Facebook page ID
    graph.put_photo(image=open(image_path, 'rb'), album_path=f"{page_id}/photos", message=post_message)

# Function to run the main process
def main():
    pages = ["Transport_in_Zambia", "Geography_of_Zambia", "List_of_populated_places_in_Zambia", "History_of_Zambia", "Ministry_of_Health_(Zambia)", "Education_in_Zambia", "Religion_in_Zambia", "Climate_of_Zambia", "National_Assembly_of_Zambia", "Zambia"]

    for page in pages:
        top_editors_data = get_top_editors(page)
        image_path = create_leaderboard_image(page, top_editors_data)
        if image_path:
            post_leaderboard_on_facebook(page, image_path, top_editors_data)
            
if __name__ == "__main__":
    main()
   