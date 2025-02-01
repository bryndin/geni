# Geni: Python Client Library for Geni.com Public REST API

[![Test](https://github.com/bryndin/geni/actions/workflows/test.yaml/badge.svg)](https://github.com/bryndin/geni/actions/workflows/test.yaml)
[![codecov](https://codecov.io/gh/bryndin/geni/graph/badge.svg?token=3Z916ZHDMK)](https://codecov.io/gh/bryndin/geni)
[![Lint](https://github.com/bryndin/geni/actions/workflows/lint.yaml/badge.svg)](https://github.com/bryndin/geni/actions/workflows/lint.yaml)
[![TypeCheck](https://github.com/bryndin/geni/actions/workflows/typecheck.yaml/badge.svg)](https://github.com/bryndin/geni/actions/workflows/typecheck.yaml)

This library simplifies interaction with the [Geni.com public REST API](https://www.geni.com/platform/developer/index), enabling developers to automate various family tree management tasks or integrate Geni functionality into their Python applications. Specifically, it helps post-process your family tree after importing a GEDCOM file.


## Features
- Simplifies API interaction.
- Implements OAuth authentication flow.
- Handles Geni's required rate-limiting automatically.
- Stores API keys and tokens for ease of use.
- Provides examples for common use cases.

## Installation
Use the following command to install the library directly from GitHub:
```bash
pip install git+https://github.com/bryndin/geni.git
```

## Usage Examples
See the [examples](./examples) directory.

## Implemented Methods
The library currently supports the following methods:

* **Profile**
  - [profile](https://www.geni.com/platform/developer/help/api?path=profile): Returns information about a profile. 
  - [add-child](https://www.geni.com/platform/developer/help/api?path=profile%252Fadd-child): Add a child to a profile and return the added profile.
  - [add-parent](https://www.geni.com/platform/developer/help/api?path=profile%252Fadd-parent): Add a parent to a profile and return the added profile.
  - [add-partner](https://www.geni.com/platform/developer/help/api?path=profile%252Fadd-partner): Add a partner to a profile and return the added profile.
  - [add-sibling](https://www.geni.com/platform/developer/help/api?path=profile%252Fadd-sibling): Add a sibling to a profile and return the added profile.
  - [delete](https://www.geni.com/platform/developer/help/api?path=profile%2Fdelete): Deletes a profile.
  - [update_basics](https://www.geni.com/platform/developer/help/api?path=profile%2Fupdate-basics): Update fields on the basics and about tabs and return the changed profile. Parameters can be posted as form data or JSON.
* **Stats**
  - [stats](https://www.geni.com/platform/developer/help/api?path=stats): Returns information about the site.
  - [world_family_tree](https://www.geni.com/platform/developer/help/api?path=stats%2Fworld-family-tree): Returns information about the world family tree.
* **User**
  - [managed_profiles](https://www.geni.com/platform/developer/help/api?path=user%2Fmanaged-profiles): Returns a list of profiles the user manages.

Additional methods are planned for future releases. Contributions are welcome!

## Authentication
To interact with the Geni API, you need to authenticate using OAuth 2.0. Follow these steps:

1. Register your application at [Geni.com App Registration](https://www.geni.com/platform/developer/help/oauth_extensions).
2. Copy your API Key.
3. Make your key available in one of the following ways:
    - Store your API Key in a file named `geni_api.key` in your working directory,
      
    - or pass your API key as a parameter during the library initialization.
4. During the first run, you will be prompted to authorize your application:
   1. In the terminal window the library will give you the URL to Geni Auth page
       ```
       Visit this URL to authorize the application:
       https://www.geni.com/platform/oauth/authorize?client_id=XXXXXXXX&response_type=token&display=desktop
       Paste the redirect URL (from the address bar):
       ```
   2. Open it in any browser and authorize your application in Geni.<br>
       ![Geni Auth Page Screenshot](./docs/_static/auth_ask.png)
   3. After authorization, Geni will redirect you to a "Not Found" page. This is expected behavior. Copy the entire URL from the browser address bar and paste it in the terminal.<br>
       ![Geni Redirect URL Location Screenshot](./docs/_static/auth_redirect_url.png)
   4. The library will extract the access token from that redirected URL and save it to a temporary file `geni_token.tmp`.

5. Each subsequent request will use the access token from the temporary file, until the token expires or the file is manually removed.
6. If the access token is expired, the library will ask you to re-authenticate before continuing with the request (expiration time is also stored in the temporary file).

## Sensitive files
The library uses two files:

- **`geni_api.key`**: Created manually to store your API key.
- **`geni_token.tmp`**: Created by the library to store the temporary API access token.

Ensure these files are secured and not exposed in version control systems. These files must be manually deleted when no longer needed.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

