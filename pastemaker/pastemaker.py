#!/usr/bin/env python3
import requests
import yaml

USER_AGENT = "PasteMaker"


def create_paste(pastebins, name, filename, flags):
    """
    Create a paste of `filename` with the paste service `name`.
    All pastebin "specifications" are taken from `pastebins`, which should be
    loaded via the YAML file.
    Options are things like the syntax, etc.. and are usually taken from argv.
    """
    paste_service = pastebins[name]
    paste_method = paste_service["method"]
    paste_result_parsing = paste_service["result_parsing"]
    method_options = paste_service["method_options"]

    for flag in paste_service["required_flags"]:
        if flag not in flags:
            raise ValueError("Missing option {!r}!".format(flag))
    for flag, default_value in paste_service["optional_flags"].items():
        flags.setdefault(flag, default_value)

    def _format(text, **extra):
        return text.format(file_contents=file_contents,
                           flags=flags,
                           constants=paste_service["constants"],
                           **extra)

    with open(filename) as fobj:
        file_contents = fobj.read()
    if paste_method == "POST":
        payload = method_options["payload"]
        if isinstance(payload, str):
            payload = _format(payload)
        else:
            for key, value in dict(payload).items():
                payload[key] = _format(value)
        response = requests.post(paste_service["url"], data=payload)
    elif paste_method == "GET":
        parameters = method_options["parameters"]
        for key, value in dict(parameters).items():
            parameters[key] = _format(value)
        response = requests.get(paste_service["url"], params=parameters)
    else:
        raise ValueError("Unknown paste method {!r}!".format(paste_method))
    response.raise_for_status()
    if paste_result_parsing["method"] == "url":
        return paste_result_parsing["format"].format(url=response.url)
    elif paste_result_parsing["json"]:
        return paste_result_parsing["method"].format_map(response.json())
    else:
        raise ValueError("Could not find result URL!")
