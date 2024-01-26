import argparse
import yaml
from typing import Dict, Optional


def load_yaml(file_name: str) -> Optional[Dict]:
    """
    Load a YAML file and return the data.

    Args:
        file_name (str): The name of the YAML file to load.

    Returns:
        Optional[Dict]: The data loaded from the YAML file or None if an error occurs.
    """
    try:
        with open(file_name, "r") as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File {file_name} not found.") from e
    except yaml.YAMLError as e:
        raise yaml.YAMLError("Error parsing YAML file.") from e


def create_diagram_lines(actions: Dict[str, Dict]) -> [str]:
    """
    Create the diagram lines from actions.

    Args:
        actions (Dict[str, Dict]): A dictionary containing the actions.

    Returns:
        List[str]: A list of diagram lines.
    """
    lines = ["graph TD"]
    for key, value in actions.items():
        # ignore actions called generate_project_dag
        if key == "generate_project_dag":
            continue
        
        lines.append(f"    {key}[{key}]")
        if value.get("needs"):
            for item in value["needs"]:
                lines.append(f"    {item} --> {key}")
    return lines


def create_mermaid_diagram(actions: Dict[str, Dict]) -> str:
    """
    Create a Mermaid diagram string based on the given actions.

    Args:
        actions (Dict[str, Dict]): A dictionary containing the actions.

    Returns:
        str: The Mermaid diagram string.
    """
    diagram_lines = create_diagram_lines(actions)
    diagram = "\n".join(diagram_lines)
    title_text = "---\ntitle: Project Pipeline\n---"  
    return f"""```mermaid\n{title_text}\n{diagram}\n```"""


def main():
    parser = argparse.ArgumentParser(
        description="Create a mermaid diagram based on actions defined in a YAML file."
    )
    parser.add_argument(
        "--yaml-path", help="Path to your YAML file.", default="project.yaml"
    )
    parser.add_argument(
        "--output-path", help="Output markdown file path.", default="project.dag.md"
    )
    args = parser.parse_args()

    try:
        data = load_yaml(args.yaml_path)
    except FileNotFoundError as e:
        print(f"File error: {e}")
        return
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}")
        return

    actions = data.get("actions", {})
    text = create_mermaid_diagram(actions)

    with open(args.output_path, "w") as text_file:
        text_file.write(text)

if __name__ == "__main__":
    main()
