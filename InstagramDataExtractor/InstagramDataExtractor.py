import instaloader
import pandas as pd
import os

# Initialize Instaloader
L = instaloader.Instaloader()

# Login (if needed)
L.login("mclicks_311", "Arun#0311")

# Choose the Instagram account to scrape
profile = instaloader.Profile.from_username(L.context, "mclicks_311")

# Create a folder to store images if it doesn't exist
image_folder = os.path.join(os.path.expanduser("~"), "Documents", "InstagramImages")
os.makedirs(image_folder, exist_ok=True)

# List to store post data
post_data = []

# Loop through the posts and extract details
for post in profile.get_posts():
    # Set image filename based on shortcode
    image_filename = os.path.join(image_folder, f"{post.shortcode}.jpg")
    
    # Check if the image already exists, skip download if it does
    if not os.path.exists(image_filename):
        # Download the image if it doesn't already exist
        L.download_pic(image_filename, post.url, post.date)
    
    # Fetch comments
    comments = [comment.text for comment in post.get_comments()]
    comment_text = " |    | ".join(comments)
    
    # Add post information to the list
    post_info = {
        "Post URL": post.url,
        "Image Path": image_filename,  # Path to the downloaded image
        "Caption": post.caption,
        "Likes": post.likes,
        "Comments": comment_text,
        "Timestamp": post.date
    }
    
    post_data.append(post_info)

# Save the data to a CSV file
output_file_path = os.path.join(os.path.expanduser("~"), "Documents", "instagram_posts.csv")
df = pd.DataFrame(post_data)
df.to_csv(output_file_path, index=False)

print("Data and images saved to", output_file_path)

# Load your existing DataFrame
df = pd.read_csv(output_file_path)

# Clean captions: Remove special characters and emojis
df['Caption'] = df['Caption'].str.replace(r'[^\w\s#@/:%.,_-]', '', regex=True)  # Keep alphanumeric and specific chars
df['Caption'] = df['Caption'].str.strip()  # Strip leading/trailing whitespace

# Clean comments: Remove special characters and emojis
df['Comments'] = df['Comments'].str.replace(r'[^\w\s#@/:%.,_-]', '', regex=True)  # Keep alphanumeric and specific chars
df['Comments'] = df['Comments'].str.strip()  # Strip leading/trailing whitespace

# # Drop rows where image_url is NaN or empty
df = df[df['Image Path'].notna() & (df['Image Path'] != '')]

# Save the cleaned DataFrame to a new CSV file
cleaned_output_file_path = os.path.join(os.path.expanduser("~"), "Documents", "cleaned_instagram_posts.csv")
df.to_csv(cleaned_output_file_path, index=False)

print(f"Cleaned data has been saved to: {cleaned_output_file_path}")
