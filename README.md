![OpenAI Web Scraping](https://img.shields.io/badge/OpenAI%20Web%20Scraping%20version-gray?style=flat)![v1.0.0](https://img.shields.io/badge/1.0.0-brightgreen?style=flat)

# OpenAI Web Scrapping Project
A simple web scrapping project using OpenAi APIs.


## How to creata a virtual environment for this projects :
First run the following command to create virtual environment.
```
python -m venv venv
```
Now run the following command to activate virtual environment(For ).
```
venv\Scripts\Activate.ps1
```

### Note: You may get error like below while running the activation command.
* venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system

In that case open Powershell as administrator and run the following command :
```
Set-ExecutionPolicy RemoteSigned
```

And then again run the activation command inside the project directory.
  
## Install required packages for the Project :
* If you don't have requirement.txt file : 
    * Run the following commamd to install required packages
        ```
        pip install requests beautifulsoup4 openai python-dotenv pandas
        ```
    * Then run the following command to list all packages in requirement.txt file
        ```
        pip freeze > requirements.txt
        ```
* If you have requirement.txt file and all required dependencies are listed in that.
    * Run the following commamd to install required packages
        ```
        pip install -r requirements.txt
        ```

## Add OpenAI key in the ".env" file: 
Create a ".env" file in the project directory and add the OpenAI key in the file as follows.
```
OPENAI_API_KEY=your_openai_api_key_here
```

You can get your OpenAI API key from the following URL: 
* https://platform.openai.com/settings/organization/api-keys