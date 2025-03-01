# [ReelRatings](https://reelratings-f616d9363755.herokuapp.com/)

![Am I Responsive](#)

(Introduction)

[View live website here](https://reelratings-f616d9363755.herokuapp.com/)

## Table of Contents

- [UX](#ux)
  - [Project Goals](#project-goals)
  - [User Stories](#user-stories)
  - [Design](#design)
  - [Wireframes](#wireframes)
- [Features](#features)
- [Database Schema](#features)
- [Manual Testing](#manual-testing)
  - [Features Testing](#features-testing)
  - [Browser Compatibility](#browser-compatibility)
  - [Responsiveness Testing](#responsiveness-testing)
  - [Accessibility Testing](#accessibility-testing)
  - [Code Validation](#code-validation)
  - [Bugs](#bugs)
  - [Lighthouse Testing](#lighthouse-testing)
- [Deployment](#deployment)
  - [Deployment (Heroku)](#deployment-heroku)
  - [Local Deployment](#local-deployment)
- [Technologies Used](#technologies-used)
  - [Languages](#languages)
  - [Design & Development Tools](#design--development-tools)
- [Credits](#credits)
  - [Code](#code)
  - [Research and Resources](#research-and-resources)
  - [Media](#media)
  - [Content](#content)

# UX

## Project Goals

- Create a platform where users can search for movies and TV shows.
- Allow users to log in and view ratings and reviews of their chosen movies/TV shows.
- Make the platform responsive and accessible across different devices and browsers.
- Use an external API to fetch data for movies and TV shows in real-time.

## User Stories

### Search Movies and TV Shows
**As a user, I can search for a specific movie or TV show by title so that I can find movies and TV shows quickly.**  


#### Acceptance Criteria:
- A search bar is available on the homepage.
- Users can enter a search term to find movies and TV shows.
- The search results display movies/TV shows matching the entered term.
- The search results include movie/TV show titles, posters, and ratings.
- The results are clickable and lead to the details page of the selected movie/TV show.

---

### Write a Review
**As a user, I can write a review for a movie or TV show so that I can share my thoughts and experiences with others.**  

#### Acceptance Criteria:
- Users can write and submit a review, including a text field.
- Reviews are stored and displayed alongside movie details.
- Each review is linked to the user who posted it.
- Reviews can be edited or deleted by the user who created them.

---

### Rate a Movie/TV Show
**As a user, I can rate a movie or TV show with a 1 to 5-star scale so that I can share my opinion and influence others’ viewing choices.**  

#### Acceptance Criteria:
- Users can give a movie or TV show a rating (1 to 5 stars).
- The rating is stored and associated with the user’s review.
- The system calculates an average rating based on all user ratings for that movie.
- The rating is visible under the movie/TV show title.

---

### Manage User Profile
**As a user, I can view and edit my profile so that I can update my information and preferences.**  

#### Acceptance Criteria:
- Users can update their email address and password.
- Users can view their movie reviews and ratings.
- The system displays a profile summary with the user’s name and activity history.

---

### Admin Access to Manage Movies and Users
**As an admin, I can manage movies, users, and reviews so that I can ensure the site content is accurate and appropriate.**  

#### Acceptance Criteria:
- Admins can view, add, edit, or delete movies.
- Admins can view and manage users’ accounts (e.g., deactivate accounts, reset passwords).
- Admins can moderate reviews and remove inappropriate content.

---

### User Registration
**As a new user, I can create an account with my email and password so that I can access the site and track movies.**  

#### Acceptance Criteria:
- Users can enter an email and password to create an account.
- The system validates the email format and password strength.
- A confirmation message is shown upon successful registration.
- The user is redirected to the homepage upon successful login.

---

### View Reviews for a Movie/TV Show
**As a user, I can view other users' reviews of a movie or TV show so that I can see different perspectives before watching.**  

#### Acceptance Criteria:
- Reviews for each movie are displayed in a list with the user’s rating.
- The reviews can be sorted by date or rating.
- Users can view the reviewer’s username and review content.

---

### User Login
**As a returning user, I can log in with my credentials so that I can access my personalised watchlist and reviews.**  

#### Acceptance Criteria:
- Users can log in using their registered email and password.
- Users can reset their password if forgotten.
- The system redirects users to the dashboard after successful login.

---

### View Movie/TV Show Details
**As a user, I can view the details of a specific movie or TV show so that I can learn more about it before deciding to watch.**  

#### Acceptance Criteria:
- Each movie detail page displays the movie's title, description, cast, genre(s), release date, and poster.
- The page also includes user reviews and ratings.
- The user can view a list of actors and crew members involved in the movie.

---

### Add a Movie/TV Show to Watchlist
**As a user, I can add movies and TV shows to my watchlist so that I can keep track of movies I want to watch later.**  

#### Acceptance Criteria:
- Users can add a movie to their watchlist by clicking an "Add to Watchlist" button.
- The movie is displayed in the user’s watchlist with an "is favourite" option.
- The watchlist page shows all the movies and TV shows the user has added.

---

### Manage Watchlist
**As a user, I can manage my watchlist (e.g., remove movies, mark favourites) so that I can customise it to my preferences.**  

#### Acceptance Criteria:
- Users can remove movies from their watchlist.
- Users can mark movies as favourites.
- The watchlist is updated in real time.


## Design

The design of ReelRatings focuses on simplicity and usability. I used a minimalistic approach with a clean layout to ensure that the content (movie ratings and reviews) is easily accessible. The user interface has been designed to be intuitive and visually appealing, using modern design principles such as card-based layouts and clear typography.

### Colour Palette

The colour palette for ReelRatings includes:
- **Vermilion**: #ed3833ff (for highlights and accents)
- **Xanthous**: #f3b743ff (for buttons and call-to-action elements)
- **Dim-Gray**: #616163ff (for text and background contrast)
- **Black**: #010101ff (for main text)
- **White**: #fefefeff (for clean backgrounds and contrast)
- **Picton-Blue**: #44aee2ff (for links and secondary elements)

### Typography

The font choices for ReelRatings are:
- **Primary Font**: **Pontiac Sans Serif Font** – A clean and modern sans-serif font, used for headings and larger text. It gives the site a bold and contemporary feel.
- **Secondary Font**: **Noyh Geometric Sans Serif Font** – A geometric sans-serif font, used for body text and general content. It provides excellent readability and complements the primary font nicely.
- **Font Sizes**: Adjusted for clarity and readability on all devices:
  - Headings: 36px for H1, 28px for H2, etc.
  - Body Text: 16px for general text

### Imagery

The imagery used in ReelRatings is focused on creating a visually appealing experience. Movie posters and images from TheMovieDB API are used to represent movies and TV shows. All images are sourced from high-quality royalty-free platforms or through the API to maintain a consistent, professional aesthetic across the application.

Additionally, the **ReelRatings logo** was designed to represent the brand's identity. The logo features a combination of key elements:
- **TV**: Representing the platform's focus on movies and TV shows.
- **Popcorn**: A fun and relatable symbol of the movie-watching experience.
- **Movie Reel**: To emphasize the connection to film and media.
- **Stars**: Symbolising ratings and reviews, as well as the entertainment industry.
- **Bold Typography**: To convey strength and reliability, ensuring the logo is easily recognizable.

You can view the logo below:

![ReelRatings Logo](static\images\logo.png)

## Wireframes

Include images of the wireframes for the main pages of the app (login, search results, movie/TV show details).

# Features

- **User Login**: Users can log in to access personalised features.
- **Search**: Users can search for movies and TV shows by title.
- **Ratings and Reviews**: Displays user ratings and reviews for movies and TV shows.
- **Responsive Layout**: The layout adjusts to different screen sizes and devices.

# Database Schema

ReelRatings uses a relational database to store user accounts, reviews, and watchlists. Below is the **Entity-Relationship Diagram (ERD)** representing the database structure:

![ERD Diagram](readme_documentation\erd\reelratings-erd.png)

## Tables

### **Users**
Stores user account details.

| Column        | Data Type  | Constraints |
|--------------|-----------|------------|
| user_id      | integer   | Primary Key |
| username     | varchar   | Unique, Not Null |
| email        | varchar   | Unique, Not Null |
| password_hash | varchar  | Not Null |
| date_joined  | timestamp | Default: current timestamp |

### **Reviews**
Stores user-submitted reviews and ratings for movies.

| Column       | Data Type  | Constraints |
|-------------|-----------|------------|
| review_id   | integer   | Primary Key |
| user_id     | integer   | Foreign Key → users.user_id |
| movie_id    | integer   | Not Null |
| rating      | integer   | Not Null (1-10 scale) |
| review_text | text      | Nullable |
| created_at  | timestamp | Default: current timestamp |

### **Watchlist**
Stores movies users have added to their watchlist, including favourites.

| Column        | Data Type  | Constraints |
|--------------|-----------|------------|
| watchlist_id | integer   | Primary Key |
| user_id      | integer   | Foreign Key → users.user_id |
| movie_id     | integer   | Not Null |
| is_favourite | boolean   | Default: false |
| added_at     | timestamp | Default: current timestamp |

## Relationships
- **Users & Reviews:** One-to-Many → A user can submit multiple reviews, but each review belongs to one user.
- **Users & Watchlist:** One-to-Many → A user can have multiple movies in their watchlist.
  
This structure ensures efficient data management and retrieval for the ReelRatings platform.

# Accessibility



# Manual Testing

## Features Testing



## User Stories Testing



## Browser Compatibility



## Responsiveness Testing



## Accessibility Testing



## Code Validation


## Bugs


## Lighthouse Testing


# Deployment

### Deployment (Heroku)

1. Clone this repository.
2. Run `pip install -r requirements.txt` to install dependencies.
3. Set up the necessary environment variables (e.g., secret key, database URL).
4. Deploy the project on [Heroku](https://www.heroku.com/).

### Local Deployment

1. Clone the repository: `git clone <repository-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the database: `python manage.py migrate`
4. Run the development server: `python manage.py runserver`

Visit `http://127.0.0.1:8000` in your browser to view the project locally.

## Technologies Used

### Languages

- HTML
- CSS
- JavaScript
- Python
- SQL

### Design & Development Tools

- Git
- GitHub
- Heroku
- Visual Studio Code

## Credits

### Code

- The movie and TV show data is fetched from the [TheMovieDB API](https://www.themoviedb.org/).

### Research and Resources

- [Bootstrap Documentation](https://getbootstrap.com/)

### Media

### Content

- Movie and TV show content sourced from TheMovieDB API.
