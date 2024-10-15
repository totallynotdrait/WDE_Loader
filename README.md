# Workspace Desktop Enviroment Loader (WDE_Loader)
WDE_Loader is a system similar to MacOS for executing an application, but in DearPyGui

## Structure

- RootDir -> Where the application files and source are
- RootDir/app.py -> Where the entry is defined, the name should always be app.py and not others. inside app.py it should always be a WDEApp class with defined the `__entry__` function
- RootDir/data.json -> Where all information about the application are defined and also some other options, all the indicated options should be defined in the JSON file
- - project_name
- - author
- - licence
- - version
- - description
- - project_website
- - author_website
- - dpgtl_style_path
- - default_icon_path
- - on_screen_keyboard
Use 0 if you don't want to define