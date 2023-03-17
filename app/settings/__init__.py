import os


def console_interface() -> list[str]:
    with open("app\\settings\\settings.txt") as settings_file:
         lines=settings_file.readlines()
    return "\n".join([line.strip() for line in lines])


def change_settings(settings_type: str, content: str) -> str:
    settings = get_all_settings()
    pre_content = settings.get(settings_type)
    if pre_content:
        if type(pre_content).__name__ == 'int':
            try:
                settings[settings_type] = int(content)
            except:
                return f"Invalid settings content - the content of \"{ settings_type }\" must be int type, while \"{ content }\" is not."
        else:
            settings[settings_type] = content
        with open("app\\settings\\settings.txt", "w") as settings_file:
            file_content = []
            for settings_name, settings_content in settings.items():
                file_content.append(f"{settings_name}({type(settings_content).__name__}): {settings_content}\n")
            settings_file.writelines(file_content)
        return "Settings was changed successfully."
    else:
        return f"Invalid settings name - there are no such as settings \"{ settings_type }\"."


def reset_to_template() -> None:
    with open("app\\settings\\template_settings.txt", "r") as settings_file:
         lines=settings_file.readlines()
    with open("app\\settings\\settings.txt", "w") as settings_file:
        settings_file.writelines(lines)


def get_settings(keyword: str) -> any:
    last_settings = get_all_settings()
    return last_settings.get(keyword)


def get_all_settings(delete_spaces=False) -> dict:
    with open("app\\settings\\settings.txt", "r") as settings_file:
         lines=settings_file.readlines()
    last_settings = {}
    try:
        for line in lines:
            if delete_spaces:
                line.replace(" ", "")
            command, value = line.split(':', 1)
            command, value_type = command.split("(")
            value_type = value_type.replace(")", "")
            if value_type == "int":
                value = int(value)
            last_settings[command] = value
    except:
        raise Exception("File \"settings.txt\" is injured.")
    return last_settings


def get_string_contain(language: str, keyword: str) -> str:
    last_settings = get_interface_text(language)
    return last_settings.get(keyword)


def get_interface_text(language: str) -> dict:
    try:
        with open(f"app\\settings\\interface_{language}.txt") as settings_file:
            lines=settings_file.readlines()
    except:
        raise Exception(f"Invalid language \"{language}\" interface. There aren`t any interface on this language.")
    last_settings = {}
    for line in lines:
        line = line.strip()
        command, value = line.split(':', 1)
        last_settings[command] = value
    return last_settings


def get_all_languages() -> list[str]:
    files = os.listdir("app\\settings")
    languages = []
    for file in files:
        if "interface_" in file:
            languages.append(file.replace("interface_", "").replace(".txt", ""))
    return languages
