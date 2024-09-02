# Starred Repositories Retriever

This project retrieves and displays your starred repositories on GitHub using OAuth authentication.

## Create your own GitHub OAuth App
1) Log in to GitHub and click your profile picture in the upper right corner. 
2) Select **Settings** from the dropdown menu.
3) Navigate to **Developer settings** and onwards to **OAuth apps**
4) Click **Register a new application** or **New OAuth App** to create a new application. 
5) Fill in the following fields:
   - Application name: Choose a name for your application
   - Homepage URL: http://127.0.0.1:8000
   - Authorization callback URL: http://127.0.0.1:8000/essential-starred-repositories-information
6) Click **Register application**
7) After creating the application, note down the **Client ID** and **Client secret**

## Clone the repository
- Clone the repository using HTTPS:
> git clone https://github.com/inkaliinalauranto/Starred-Repositories-Retriever.git
- Open the project in your preferred editor 

## Create a virtual environment
- Navigate to the root folder of the project in your editor's terminal and create a virtual environment: 
> python -m venv .venv
- Activate the virtual environment (on Windows):
> .venv\Scripts\activate

## Install required libraries
- With the virtual environment activated, install the required libraries:
> python -m pip install -r requirements.txt

## Configure environment variables
- Create a .env-named file in the root folder of the project
- Open the .env file and add the following lines:
```
ID=Your_GitHub_ID_here
SECRET=Your_GitHub_secret_here
```
- Replace "Your_GitHub_ID_here" and "Your_GitHub_secret_here" with your GitHub OAuth application's Client ID and Client secret

## Start the web server:
- Run the following command to start the server with FastAPI:
> uvicorn main:app --reload


## Access the application
- Open your web browser and navigate to http://127.0.0.1:8000/login
- Authenticate via the GitHub OAuth interface to view your starred repositories
- For a better view of the JSON data, consider installing a JSON Formatter extension in your browser
