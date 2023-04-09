import json
import click
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


@click.command()
def next_slide():
    current_position = int(config.get("position", "current"))
    with open("intro.json", "r") as json_file:
        data = json.load(json_file)

    slide = list(data.keys())[current_position - 1]
    title = data[slide].get("title", "")
    content = (
        data[slide].get("content", "").split("\n")
        if len(data[slide].get("content", "").split("\n")) > 1
        else data[slide].get("content", "").split(".")
    )
    speaker_notes = data[slide].get("speaker_notes", "").split(".")

    with open("main.py", "a") as main_file:
        main_file.write(f"# {title.upper()}\n\n")
        if len(content) > 2:
            for line in content:
                if line.startswith("```") or line.startswith("```bash") or line.startswith("python"):
                    continue
                elif line.startswith("PS"):
                    main_file.write(f"\n#\t{line.strip()}\n")
                else:
                    main_file.write(f"# {line.strip()}\n") if line.strip() else None
        main_file.write("\n######\n\n")

    with open("speaker_notes.txt", "a") as notes_file:
        notes_file.write(f"{slide}\n")
        notes_file.write(f"{title.strip}\n")
        for line in speaker_notes:
            notes_file.write(f"{line}\n")
        notes_file.write("\n\n    ~~~~~~~~    \n\n")

    config.set("position", "current", str(current_position + 1))
    with open("config.ini", "w") as config_file:
        config.write(config_file)

    click.echo(f"Processed slide: {slide}")


@click.command()
def reset():
    config.set("position", "current", "1")
    with open("config.ini", "w") as config_file:
        config.write(config_file)

    with open("main.py", "w") as main_file:
        main_file.write("")

    with open("speaker_notes.txt", "w") as notes_file:
        notes_file.write("")

    click.echo("Reset complete")


if __name__ == "__main__":
    next_slide()
