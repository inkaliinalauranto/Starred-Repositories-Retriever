from fastapi import APIRouter, Response
from dotenv import load_dotenv
import os
from fastapi.responses import RedirectResponse
import httpx

repositories_router = APIRouter(tags=["repositories"])

# Create a .env file in the root of the project and add your GitHub OAuth
# client ID and secret there.

# Loading environment variables from the .env file:
load_dotenv(dotenv_path=".env")

# Retrieving OAuth credentials from environment variables:
client_id = os.environ.get("ID")
client_secret = os.environ.get("SECRET")

# If the credentials are not found, an error is raised to inform that the
# environment variables are missing:
if not client_id or not client_secret:
    raise ValueError(
        "GitHub OAuth credentials missing. Please set ID and SECRET in the "
        ".env file."
    )


'''The logic of the GET routers was inspired by Estes' 2023 tutorial video: 
https://www.youtube.com/watch?v=Pm938UxLEwQ.'''


@repositories_router.get('/login')
async def login(response: Response):
    try:
        # The /login endpoint redirects the client to GitHub's OAuth
        # authorization page where the use can authorize the application to
        # access their data:
        return RedirectResponse(
            f"https://github.com/login/oauth/authorize?client_id={client_id}"
        )
    except Exception as e:
        # If any error occurs during the redirect process, the response status
        # is set to Internal Server Error and the error is returned as a
        # response:
        response.status_code = 500
        return {"Error": str(e)}


# The endpoint is accessed after login and displays the user's starred
# repositories. The usage of the httpx library and FastAPI's Response
# was inspired by Hiltunen's 2023 example project at
# https://peke.plab.fi/matias.hiltunen/todo-with-ai-images-example:
@repositories_router.get('/essential-starred-repositories-information')
async def show_starred_repositories(code: str, response: Response):
    # Define query parameters for the GitHub OAuth access token request:
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code
    }
    print(code)
    # Set the Accept header to request JSON format from GitHub's API:
    headers = {"Accept": "application/json"}

    # Use the httpx to create an asynchronous HTTP client:
    async with httpx.AsyncClient() as client:
        # Request the access token from GitHub's OAuth endpoint:
        access_token_res = await client.post(
            url="https://github.com/login/oauth/access_token",
            params=params,
            headers=headers
        )
        # If the request fails, an error response with the status code and
        # a message are returned:
        if access_token_res.status_code != 200:
            response.status_code = access_token_res.status_code
            return {"Error": "Access token retrieving failed."}

        # Otherwise, extract the access token from the response:
        access_token = access_token_res.json().get("access_token")
        if not access_token:
            # Return an error if the access token is missing:
            response.status_code = 400
            return {"Error": "Access token missing."}

        # Add the access token to the header:
        headers.update({"Authorization": f"Bearer {access_token}"})

        # Retrieve the user's information using the header with the access
        # token:
        user_info_res = await client.get(
            url="https://api.github.com/user",
            headers=headers
        )
        # If the request fails, return an error response with the status code:
        if user_info_res.status_code != 200:
            response.status_code = user_info_res.status_code
            return {"Error": "Failed to retrieve user information."}

        # Convert the response to json and extract the user's username
        # (key: login):
        user = user_info_res.json().get("login")

        # Retrieve the user's starred repositories:
        starred_repos_res = await client.get(
            url=f"https://api.github.com/users/{user}/starred",
            headers=headers
        )
        # If the request fails, return an error response with the status code:
        if starred_repos_res.status_code != 200:
            response.status_code = starred_repos_res.status_code
            return {"Error": "Failed to retrieve starred repositories information."}

        # Convert the response to json:
        starred_repos_info = starred_repos_res.json()
        # Initialize a list to store the essential information for each
        # repository:
        essential_repos_info = []

        # Iterate over the starred repositories:
        for repo in starred_repos_info:
            # Skip private repositories:
            if not repo.get("private"):

                # Extract the essential repository information:
                repo_dict = {
                    "name": repo.get("name"),
                    "description": repo.get("description"),
                    "URL": repo.get("html_url"),
                    "topics": repo.get("topics")
                }

                # If the repository has a license, insert it into the
                # repo_dict dictionary before the topics-key.
                if repo.get("license") is not None:
                    license_index = list(repo_dict.keys()).index("topics")
                    repo_items = list(repo_dict.items())
                    repo_items.insert(
                        license_index, ("license", repo.get("license").get("name"))
                    )
                    repo_dict = dict(repo_items)

                # Add the repository's essential information to the list:
                essential_repos_info.append(repo_dict)

        return {
            # Return the count of starred repositories (private or not) and
            # the essential information of the public repositories
            "starred_repositories_count": len(starred_repos_info),
            "starred_repositories": essential_repos_info
        }
