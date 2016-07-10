#!/usr/bin/env python3
import requests
import yaml

USER_AGENT = "PasteMaker"


def create_paste(pastebins, name, filename, options):
    """
    Create a paste of `filename` with the paste service `name`.
    All pastebin "specifications" are taken from `pastebins`, which should be
    loaded via the YAML file.
    Options are things like the syntax, etc.. and are usually taken from argv.
    """
    paste_service = pastebins[name]
    paste_method = paste_service["method"]
    paste_result_in = paste_service["result_in"]
    method_options = paste_service["method_options"]

    for option in paste_service["required_options"]:
        if option not in options:
            raise ValueError("Missing option {!r}!".format(option))

    with open(filename) as fobj:
        file_contents = fobj.read()
    if paste_method == "POST":
        payload = method_options["payload"]
        if isinstance(payload, str):
            payload = payload.format(file_contents=file_contents,
                                     options=options,
                                     constants=paste_service["constants"])
        else:
            for key, value in dict(payload).items():
                payload[key] = value.format(file_contents=file_contents,
                                            options=options,
                                            constants=paste_service["constants"])
        response = requests.post(paste_service["url"], data=payload)
    elif paste_method == "GET":
        parameters = method_options["parameters"]
        for key, value in dict(parameters).items():
            parameters[key] = value.format(file_contents=file_contents,
                                           options=options,
                                           constants=paste_service["constants"])
        response = requests.get(paste_service["url"], params=parameters)
    else:
        raise ValueError("Unknown paste method {!r}!".format(paste_method))
    response.raise_for_status()
    if paste_result_in == "page":
        return response.text
    elif paste_result_in == "url":
        return response.url
    else:
        raise ValueError("Could not find result URL, was meant to look in"
                         " {!r}".format(paste_result_in))
