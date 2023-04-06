import json
import click
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

@click.command()
def next_slide():
    current_position = int(config.get("position", "current"))
    with open("intro-to-python.json", "r") as json_file:
        data = json.load(json_file)

    slide = list(data.keys())[current_position - 1]

    content = data[slide].get("content", "").split("\n")
    speaker_notes = data[slide].get("speaker_notes", "")

    with open("main.py", "a") as main_file:
        main_file.write(f"# {slide}\n")
        main_file.write(f"# {content}\n")
        main_file.write("\n\n    ~~~~~~~~    \n\n")

    with open("speaker_notes.txt", "a") as notes_file:
        notes_file.write(f"{slide}\n")
        notes_file.write(speaker_notes)
        notes_file.write("\n\n    ~~~~~~~~    \n\n")

    config.set("position", "current", str(current_position + 1))
    with open("config.ini", "w") as config_file:
        config.write(config_file)

    click.echo(f"Processed slide: {slide}")

if __name__ == "__main__":
    next_slide()
